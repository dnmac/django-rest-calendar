from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .models import Calendar, UserEvent, CurrentWeek, CurrentWeekEvent

User = get_user_model()


class CurrentWeekInline(admin.TabularInline):
    model = CurrentWeek


class CurrentWeekEventInline(admin.TabularInline):
    model = CurrentWeekEvent


class CalendarAdmin(admin.ModelAdmin):
    model = Calendar
    search_fields = ['user']


class CurrentWeekAdmin(admin.ModelAdmin):
    model = CurrentWeek
    # inlines = [CurrentWeekEventInline]

    list_display = ('calendar', 'week_number',)
    autocomplete_fields = ['calendar']
    readonly_fields = ['year_number', 'month_number', 'week_number', ]
    list_filter = ('calendar', 'week_number',)
    search_fields = ('calendar__name', 'week_number',)


class CurrentWeekEventAdmin(admin.ModelAdmin):

    def calendar(self, instance):
        try:
            return instance.current_week.calendar
        except ObjectDoesNotExist:
            return 'ERROR!!'

    model = CurrentWeekEvent
    fk_links = ['user', 'current_week', ]
    readonly_fields = [
                    'day', 'day_number', 'week_number', 'month_number',
                    'start_date', 'end_date', 'calendar'
                    ]
    list_display = ('title', 'calendar', 'week_number')
    list_filter = ('calendar', 'week_number',)
    search_fields = ('title', 'calendar__name', )


admin.site.register(UserEvent)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(CurrentWeek, CurrentWeekAdmin)
admin.site.register(CurrentWeekEvent, CurrentWeekEventAdmin)
