from rest_framework import permissions


def is_superadmin_user(user):
    return bool(user and user.is_authenticated and (getattr(user, 'role', None) == 'super_admin' or user.is_superuser))


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_superadmin_user(request.user)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_superadmin_user(request.user):
            return True
        return bool(
            request.user and request.user.is_authenticated and 
            request.user.role in ['super_admin', 'admin']
        )


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_superadmin_user(request.user):
            return True
        return bool(
            request.user and request.user.is_authenticated and 
            request.user.role in ['super_admin', 'admin', 'teacher']
        )


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_superadmin_user(request.user):
            return True
        return bool(
            request.user and request.user.is_authenticated and 
            request.user.role in ['student', 'super_admin', 'admin']
        )


class IsCenterOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_superadmin_user(request.user):
            return True
        return bool(
            request.user and request.user.is_authenticated and 
            request.user.role in ['super_admin', 'admin', 'center_owner']
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow owners or Superadmins to edit an object.
    """
    def has_permission(self, request, view):
        if is_superadmin_user(request.user):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if is_superadmin_user(request.user):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            if hasattr(obj, 'owner') and obj.owner == request.user:
                return True
            if hasattr(obj, 'user') and obj.user == request.user:
                return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_superadmin_user(request.user):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role in ['super_admin', 'admin'])

