from django.urls import path, include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from calendars.urls import router as calendarrouter
from accounts.urls import router as accountsrouter

router = DefaultRouter()

router.registry.extend(calendarrouter.registry)
router.registry.extend(accountsrouter.registry)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('calendars/', include('calendars.urls')),
    path('accounts/', include('accounts.urls')),
]
