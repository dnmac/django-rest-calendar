class EventMixin(object):
    """
    Common mixin for events and invitations
    """
    ALL_DAY = 'AD'
    MORNING = 'AM'
    EVENING = 'PM'
    TYPE_CHOICES = (
        (ALL_DAY, 'All day'),
        (MORNING, 'AM'),
        (EVENING, 'PM'),
    )


class EventPriority(object):
    """
    Mixin for event priority
    """
    EVENT_PRIORITY_CHOICES = (
        ('A', 'High Priority'),
        ('B', 'Mid Priority'),
        ('C', 'Low Priority'),
    )
