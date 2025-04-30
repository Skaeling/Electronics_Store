from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = "You don't have superuser rights to perform this actions"

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsActiveStuff(permissions.BasePermission):
    message = "Only active stuff users can use this API"

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)


class IsUser(permissions.BasePermission):
    message = "Данный профиль вам не принадлежит"

    def has_object_permission(self, request, view, obj):
        return obj == request.user
