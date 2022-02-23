from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'calendars'
router = routers.DefaultRouter()

router.register('api/admin/calendars', views.CalendarAdminViewSet,
                basename='calendar-admin')
router.register('api/admin/events', views.EventAdminViewSet,
                basename='event-admin')
router.register('calendar', views.CalendarOwnedViewSet,
                basename='calendar')
router.register('events', views.EventOwnedViewSet, basename='event-owned')
router.register('eventslist', views.EventList, basename='event-list')
router.register('eventslist/monthview', views.EventMonthView,
                basename='event-month-view')
router.register('eventslist/allview', views.EventAllView,
                basename='event-all-view')
router.register('eventslist/currentweek', views.CurrentWeekView)
router.register('eventslist/currentweekall', views.CurrentWeekAllView,
                basename='current-week')

urlpatterns = [
    path('', include(router.urls)),
]
