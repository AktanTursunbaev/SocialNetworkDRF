from rest_framework import permissions


class IsPostOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, post):
        if request.method in permissions.SAFE_METHODS:
            return True
        return post.user == request.user


class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, post):
        return post.user == request.user
