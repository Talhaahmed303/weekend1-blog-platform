from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from .models import Category, Post
from .serializers import (
    CategorySerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostWriteSerializer
)
from .permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().annotate(posts_count_annotated=Count('posts'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'category__name', 'author__username']
    ordering_fields = ['created_at', 'published_at', 'title']
    ordering = ['-published_at', '-created_at']

    def get_queryset(self):
        user = self.request.user
        qs = Post.objects.select_related('author', 'category').annotate(
            comments_count_annotated=Count('comments')
        )

        # Base visibility rules
        if not user or not user.is_authenticated:
            qs = qs.filter(status='published')
        elif getattr(user, 'role', '') == 'admin' or user.is_staff or user.is_superuser:
            pass  # Admin can see everything
        else:
            # Author can see all published + their own drafts
            qs = qs.filter(Q(status='published') | Q(author=user))

        # Query param filtering
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        author_id = self.request.query_params.get('author')
        if author_id:
            qs = qs.filter(author_id=author_id)

        status_param = self.request.query_params.get('status')
        if status_param and status_param in ['draft', 'published']:
            # If requesting drafts, ensure authorization
            if status_param == 'draft':
                if not user or not user.is_authenticated:
                    return Post.objects.none()
                if getattr(user, 'role', '') != 'admin' and not user.is_staff:
                    qs = qs.filter(author=user, status='draft')
                else:
                    qs = qs.filter(status='draft')
            else:
                qs = qs.filter(status='published')

        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostWriteSerializer

    def perform_create(self, serializer):
        status_val = serializer.validated_data.get('status', 'draft')
        published_at = timezone.now() if status_val == 'published' else None
        serializer.save(author=self.request.user, published_at=published_at)

    def perform_update(self, serializer):
        instance = serializer.instance
        new_status = serializer.validated_data.get('status', instance.status)
        if new_status == 'published' and not instance.published_at:
            serializer.save(published_at=timezone.now())
        elif new_status == 'draft':
            serializer.save(published_at=None)
        else:
            serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, id=None):
        post = self.get_object()
        # Ensure ownership
        if post.author != request.user and getattr(request.user, 'role', '') != 'admin' and not request.user.is_staff:
            return Response(
                {"success": False, "message": "You do not have permission to publish this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        post.status = 'published'
        post.published_at = timezone.now()
        post.save()
        return Response({
            "success": True,
            "message": "Post published successfully",
            "data": PostDetailSerializer(post).data
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unpublish(self, request, id=None):
        post = self.get_object()
        if post.author != request.user and getattr(request.user, 'role', '') != 'admin' and not request.user.is_staff:
            return Response(
                {"success": False, "message": "You do not have permission to unpublish this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        post.status = 'draft'
        post.published_at = None
        post.save()
        return Response({
            "success": True,
            "message": "Post reverted to draft",
            "data": PostDetailSerializer(post).data
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        user = request.user
        qs = Post.objects.filter(author=user).select_related('author', 'category').annotate(
            comments_count_annotated=Count('comments')
        )
        serializer = PostListSerializer(qs, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })
