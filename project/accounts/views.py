from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()


class UserCreate(generics.CreateAPIView):
    """View for user registration."""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )


class UserAdminViewSet(viewsets.ModelViewSet):
    """Convenience API view for viewing all data for the admin."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
