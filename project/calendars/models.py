from django.db import models, IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.utils import timezone as _timezone
from .choices import EventPriority, EventMixin


User = get_user_model()


class Calendar(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=User)

    def __str__(self):
        return str(self.name)


class Event(models.Model):

    class Meta:
        abstract = True

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    duration = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    start_date = models.DateField(default=_timezone.now)
    end_date = models.DateField(default=_timezone.now)
    week_number = models.IntegerField(default=0)
    month_number = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.week_number = self.start_date.isocalendar()[1]
        self.month_number = self.start_date.strftime("%m")
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title + " : " + str(self.start_date))


class UserEvent(Event):

    priority = models.CharField(
                                max_length=3,
                                choices=EventPriority.EVENT_PRIORITY_CHOICES,
                                blank=True
    )
    type = models.CharField(
                            max_length=3,
                            choices=EventMixin.TYPE_CHOICES,
                            default=EventMixin.MORNING
    )

    def __str__(self):
        return self.title


class CurrentWeek(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                                    fields=['calendar', 'week_number'],
                                    name='unique_week'
            ),
            models.UniqueConstraint(
                                    fields=['calendar', 'start_date'],
                                    name='unique_start'
            ),
            models.UniqueConstraint(
                                    fields=['week_number', 'start_date'],
                                    name='unique_week_start'
            )
        ]

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE,)
    start_date = models.DateField(default=_timezone.now)
    year_number = models.IntegerField(default=0)
    month_number = models.IntegerField(default=0)
    week_number = models.IntegerField(default=0)

    def __str__(self):
        return str(f'{self.calendar.user.email}: Week number: {self.week_number}')

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.year_number = self.start_date.isocalendar()[0]
                self.month_number = self.start_date.strftime("%m")
                self.week_number = self.start_date.isocalendar()[1]
                super(CurrentWeek, self).save(*args, **kwargs)
        except IntegrityError:
            pass


class CurrentWeekEvent(Event):
    """ Model used by engine for writing training week,
     inherits from Event parent is Calendar """
    current_week = models.ForeignKey(
                                    CurrentWeek,
                                    on_delete=models.CASCADE,
                                    related_name="currentweekevent",
                                    )

    comments = models.CharField(max_length=250, blank=True)
    day = models.CharField(max_length=10, blank=True)
    day_number = models.IntegerField(default=0)
