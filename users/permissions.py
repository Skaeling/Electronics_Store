from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = "You don't have superuser rights to perform this actions"

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsActiveUser(permissions.BasePermission):
    message = "Yours account isn't active, please contact your system administrator in case of any misunderstanding"

    def has_permission(self, request, view):
        return request.user.is_active
