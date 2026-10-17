from rest_framework import permissions

class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Anyone can read published posts.
    - Draft posts are only visible to the post's author or admins.
    - Write operations require authentication.
    - Updating / Deleting requires being the author or an admin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.status == 'published':
                return True
            # Draft: only author or admin
            if not request.user or not request.user.is_authenticated:
                return False
            return obj.author == request.user or getattr(request.user, 'role', '') == 'admin' or request.user.is_staff

        # Write operations: Only author or admin
        if not request.user or not request.user.is_authenticated:
            return False
        return obj.author == request.user or getattr(request.user, 'role', '') == 'admin' or request.user.is_staff

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access for anyone, but write access only to admins.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            (getattr(request.user, 'role', '') == 'admin' or request.user.is_staff)
        )
