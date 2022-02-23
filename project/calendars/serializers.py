from datetime import datetime
from rest_framework import serializers
from .models import Calendar, UserEvent, CurrentWeekEvent


class CalendarSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for calendar model."""

    class Meta:
        model = Calendar
        fields = ('user', 'id', 'name',)


class CalendarOwnedSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for calendar model."""

    class Meta:
        model = Calendar
        fields = ('id', 'name')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """Event serializer for admins."""

    id = serializers.ReadOnlyField()

    start_date = serializers.DateField(
        input_formats=['%Y-%m-%d'], format=None, allow_null=True,
        help_text='Accepted format is YYYY/MM/DD',
        style={'input_type': 'text', 'placeholder': '2022-01-30'},
    )

    end_date = serializers.DateField(
        input_formats=['%Y-%m-%d'], format=None, allow_null=True,
        help_text='Accepted format is YYYY/MM/DD',
        style={'input_type': 'text', 'placeholder': '2022-01-30'},
    )

    class Meta:
        model = UserEvent
        fields = ('id',  'calendar', 'title', 'description',
                  'priority', 'type', 'start_date', 'end_date', 'duration',)
        read_only_fields = ('week_number',)


class EventOwnedSerializer(serializers.ModelSerializer):
    """Serializer for user generated events, model=UserEvent."""

    id = serializers.ReadOnlyField()
    calendar = serializers.HyperlinkedRelatedField(
                                                   many=False,
                                                   view_name='calendar-detail',
                                                   read_only=True
                                                )
    start_date = serializers.DateField(
                                    input_formats=['%Y-%m-%d'], format=None,
                                    allow_null=True,
                                    help_text='Accepted format is YYYY-MM-DD',
                                    style={
                                        'input_type': 'text',
                                        'placeholder': '2022-01-30'
                                    },
    )

    end_date = serializers.DateField(
                                    input_formats=['%Y-%m-%d'],
                                    format=None,
                                    allow_null=True,
                                    help_text='Accepted format is YYYY-MM-DD',
                                    style={
                                        'input_type': 'text',
                                        'placeholder': '2022-01-30'
                                    },
    )

    class Meta:
        model = UserEvent
        fields = (
                'id',   'title', 'description', 'week_number', 'month_number',
                'calendar', 'priority',  'type', 'start_date', 'end_date', 'duration',
                )
        read_only_fields = ('calendar_id', 'week_number', 'month_number', )

    def validate(self, attrs):
        if "start_date" in attrs and "end_date" in attrs:
            if attrs["end_date"] < attrs["start_date"]:
                raise serializers.ValidationError({
                    "date validation": "End date must be greater than start date",
                })

        return super(EventOwnedSerializer, self).validate(attrs)

    def save(self, **kwargs):
        start_date = self.validated_data.get('start_date', datetime.now())
        end_date = self.validated_data.get('end_date', datetime.now())
        week_number = self.validated_data.get('week_number')
        month_number = self.validated_data.get('month_number')
        calendar = self.validated_data.get('calendar')
        self.validated_data['calendar'] = calendar
        self.validated_data['week_number'] = week_number
        self.validated_data['month_number'] = month_number
        self.validated_data['start_date'] = start_date
        self.validated_data['end_date'] = end_date

        super(EventOwnedSerializer, self).save(**kwargs)

    def create(self, validated_data):
        return UserEvent.objects.create(**validated_data)


class CurrentWeekEventSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for CurrentWeek Events."""

    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='current-week-detail',
    )

    class Meta:
        model = CurrentWeekEvent
        fields = (
                'id',  'week_number', 'url',  'calendar', 'title', 'description',
                'start_date', 'end_date', 'comments', 'duration',
                )
        read_only_fields = (
                            'id', 'week_number', 'url', 'week_number', 'calendar',
                            'title', 'start_date', 'end_date',
                            )
