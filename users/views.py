from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserCreateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Создает новый профиль пользователя"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновляет профиль пользователя, если user обладает правами администратора"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (IsAdmin,)
