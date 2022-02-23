from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('api/users', views.UserAdminViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserCreate.as_view())
]
