
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from core.helpers import get_dates
from .models import Calendar, CurrentWeekEvent, CurrentWeek


User = get_user_model()


# Calendar create signals
@receiver(post_save, sender=User)
def create_calendar(instance, created, **kwargs):

    if created:
        Calendar.objects.create(user=instance, name=instance.username)
        print('User Calendar created!')


# CurrentWeekEvent create signals
@receiver(post_save, sender=CurrentWeek)
def create_currentweekevents(instance, created, **kwargs):

    dates = get_dates(instance.start_date)

    if created:
        for i in range(7):
            CurrentWeekEvent.objects.get_or_create(
                current_week=instance, day_number=i, day=dates[i].strftime(
                    '%A'),
                start_date=dates[i], end_date=dates[i],
                calendar_id=instance.calendar_id,
                title=f'Event, {i}'
            )

        print('CurrentWeekEvent Created!')
