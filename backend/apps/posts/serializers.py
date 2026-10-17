from rest_framework import serializers
from .models import Category, Post
from apps.authentication.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'posts_count', 'created_at')
        read_only_fields = ('id', 'slug', 'created_at')

    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'slug', 'excerpt', 'cover_image',
            'status', 'author', 'category', 'comments_count',
            'published_at', 'created_at', 'updated_at'
        )

    def get_comments_count(self, obj):
        return getattr(obj, 'comments_count_annotated', obj.comments.count())

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'slug', 'content', 'excerpt', 'cover_image',
            'status', 'author', 'category', 'comments_count',
            'published_at', 'created_at', 'updated_at'
        )

    def get_comments_count(self, obj):
        return obj.comments.count()

class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'category', 'status', 'cover_image', 'slug')
        read_only_fields = ('id', 'slug')

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value.strip()
