from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from apps.posts.models import Post

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        qs = Comment.objects.select_related('author', 'post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        
        # Don't show comments on draft posts to unauthorized users
        user = self.request.user
        if not user or not user.is_authenticated:
            qs = qs.filter(post__status='published')
        elif getattr(user, 'role', '') != 'admin' and not user.is_staff:
            from django.db.models import Q
            qs = qs.filter(Q(post__status='published') | Q(post__author=user))
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.validated_data['post']
        if post.status != 'published':
            raise ValidationError({"post": "Cannot add comments to unpublished draft posts."})
        comment = serializer.save(author=request.user)
        # Return full CommentSerializer containing author object
        out_serializer = CommentSerializer(comment)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user
        is_comment_author = comment.author == user
        is_post_author = comment.post.author == user
        is_admin = getattr(user, 'role', '') == 'admin' or user.is_staff
        
        if not (is_comment_author or is_post_author or is_admin):
            raise PermissionDenied("You do not have permission to delete this comment.")
        
        comment.delete()
        return Response({"success": True, "message": "Comment deleted successfully"}, status=status.HTTP_200_OK)
