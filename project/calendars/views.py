from rest_framework import viewsets, permissions, mixins, authentication
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_multiple_model.views import ObjectMultipleModelAPIView
from .models import Calendar, UserEvent, CurrentWeekEvent
from . filters import IsOwnerFilterBackend, IsEventCalendarOwnerFilterBackend,\
    EventListFilter, CurrentMonthFilterBackend, CurrentWeekFilterBackend,\
    CalendarFilterBackend
from .serializers import CalendarSerializer, EventSerializer,\
    EventOwnedSerializer, CalendarOwnedSerializer,\
    CurrentWeekEventSerializer


class AuthMixin:
    """Provides authentication and permissions."""

    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)


class CalendarAdminViewSet(AuthMixin, viewsets.ModelViewSet):
    """
    Convenience API view for viewing all data for the admin
    and all operations
    """
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    permission_classes = (permissions.IsAdminUser,)


class EventAdminViewSet(AuthMixin, viewsets.ModelViewSet):
    """
    Convenience API view for viewing all data for the admin
    and all operations
    """
    queryset = UserEvent.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAdminUser,)


class CalendarOwnedViewSet(AuthMixin, viewsets.ModelViewSet):
    """
    API view for displaying only calendars that are the current user's
    """
    filter_backends = (IsOwnerFilterBackend,)
    serializer_class = CalendarOwnedSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self, *args, **kwargs):
        return Calendar.objects.all().filter(user=self.request.user)


class EventOwnedViewSet(AuthMixin, viewsets.ModelViewSet):
    """
    API view for displaying only UserEvents that are the current user's
    """
    serializer_class = EventOwnedSerializer
    filter_backends = (
            IsEventCalendarOwnerFilterBackend,
            CalendarFilterBackend
            )

    def get_queryset(self, *args, **kwargs):
        return UserEvent.objects.all().filter(calendar__user=self.request.user)

    def perform_create(self, serializer):
        calendar = Calendar.objects.get(user=self.request.user)

        serializer.save(calendar_id=calendar.id)


class EventMonthView(
                    AuthMixin,
                    ObjectMultipleModelAPIView,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet
                     ):
    """User events for the current month."""

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        IsEventCalendarOwnerFilterBackend,
        CurrentMonthFilterBackend,
        )
    pagination_class = None
    querylist = [
            {
                'queryset': UserEvent.objects.order_by('-start_date'),
                'serializer_class': EventOwnedSerializer
            },
            {
                'queryset': CurrentWeekEvent.objects.order_by('-start_date'),
                'serializer_class': CurrentWeekEventSerializer
            },
    ]

    @classmethod
    def get_extra_actions(cls):
        return []


class EventList(AuthMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet
                ):
    """
    API view for displaying only UserEvents that are the current user's
    Filtering enabled
    """
    serializer_class = EventOwnedSerializer
    queryset = UserEvent.objects.all()
    filter_backends = (
                        DjangoFilterBackend,
                        SearchFilter,
                        OrderingFilter,
                        IsEventCalendarOwnerFilterBackend,
                        CalendarFilterBackend,
                        )
    filterset_class = EventListFilter
    search_fields = ('title', 'description')
    ordering_fields = ['start_date', 'month_number']
    ordering = ['start_date']

    @classmethod
    def get_extra_actions(cls):
        return []

    def get_queryset(self, *args, **kwargs):
        return UserEvent.objects.all().filter(calendar__user=self.request.user)


class CurrentWeekView(AuthMixin, viewsets.ModelViewSet):
    """API view for displaying This week's CurrentWeekEvents"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CurrentWeekEventSerializer
    queryset = CurrentWeekEvent.objects.all()
    filter_backends = (
                    CurrentWeekFilterBackend,
                    IsEventCalendarOwnerFilterBackend
                    )
    http_method_names = ['get', 'put']

    @classmethod
    def get_extra_actions(cls):
        return []


class CurrentWeekAllView(AuthMixin, viewsets.ModelViewSet):
    """
    API view for displaying ALL "CurrentWeek" generated events, user specific.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CurrentWeekEventSerializer
    queryset = CurrentWeekEvent.objects.all()
    filter_backends = (IsEventCalendarOwnerFilterBackend,)
    http_method_names = ['get', 'put']


class EventAllView(
                AuthMixin,
                ObjectMultipleModelAPIView,
                mixins.ListModelMixin,
                viewsets.GenericViewSet
                ):
    """ All events: User/CurrentWeek."""

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (
                        DjangoFilterBackend,
                        SearchFilter,
                        IsEventCalendarOwnerFilterBackend
                    )

    pagination_class = None
    querylist = [
            {
                'queryset': UserEvent.objects.order_by('-start_date'),
                'serializer_class': EventOwnedSerializer
            },
            {
                'queryset': CurrentWeekEvent.objects.order_by('-start_date'),
                'serializer_class': CurrentWeekEventSerializer
            },
    ]
