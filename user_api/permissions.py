from rest_framework import status, permissions
from rest_framework.permissions import BasePermission, IsAdminUser

from .models import User


class IsAdmin(IsAdminUser):    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == User.ADMIN or request.user.is_superuser


class IsOwnerOrAdminOrModeratorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author == request.user or 
            request.method in permissions.SAFE_METHODS or 
            request.user.role == User.ADMIN or 
            (request.method in ['GET', 'DELETE'] and request.user.role == User.MODERATOR)
            )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return bool(
                request.user.role == User.ADMIN or
                request.user.is_superuser
            )
            
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.role == User.ADMIN or request.user.is_superuser

        return False
            