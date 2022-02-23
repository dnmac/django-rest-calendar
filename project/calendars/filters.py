from datetime import datetime
from django.db.models import Q
from rest_framework import filters
from django_filters.widgets import RangeWidget
import django_filters
from . models import UserEvent, CurrentWeekEvent, Calendar


class EventListFilter(django_filters.FilterSet):
    """
    FilterSet for filtering events between dates
    """
    date_between = django_filters.DateFromToRangeFilter(
                                                        field_name='start_date',
                                                        label='Date range',
                                                        widget=RangeWidget(
                                                                attrs={'type': 'date'}
                                                                )
                                                        )

    class Meta:
        model = UserEvent
        fields = ['id', 'week_number', 'month_number', 'calendar']


class CurrentMonthFilterBackend(django_filters.FilterSet):
    """
    FilterSet for filtering events between dates
    """
    date = datetime.now()
    current_month = date.today().strftime("%m")

    class Meta:
        model = UserEvent
        fields = ['month_number']

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(month_number=self.current_month)


class CurrentWeekFilterBackend(filters.BaseFilterBackend):
    """
    FilterSet for filtering events for the current week
    """
    class Meta:
        model = CurrentWeekEvent
        fields = ['week_number']

    date = datetime.now()
    current_week = date.isocalendar()[1]

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(week_number=self.current_week)


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter for getting only owned objects
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class IsEventCalendarOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter for getting only owned objects, for Events
    """
    class Meta:
        model = Calendar
        fields = ['owner']

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(calendar__user=request.user),)


class CalendarFilterBackend(filters.BaseFilterBackend):
    """
    Filter events based on user calendar
    """
    class Meta:
        model = Calendar
        fields = ['calendar']

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(calendar__user=request.user),)
