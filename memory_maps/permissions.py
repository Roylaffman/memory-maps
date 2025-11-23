"""
Custom permissions for memory_maps app.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a map to edit it.
    Public maps can be read by anyone.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for public maps
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or obj.owner == request.user
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user
