from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Show(models.Model):
    WEEKDAYS = [
        ('mon', _('Monday')),
        ('tue', _('Tuesday')),
        ('wed', _('Wednesday')),
        ('thu', _('Thursday')),
        ('fri', _('Friday')),
        ('sat', _('Saturday')),
        ('sun', _('Sunday')),
    ]

    AUDIENCE_TYPES = [
        ('niños', _('Children')),
        ('adultos', _('Adults')),
        ('todo_publico', _('All audiences')),
    ]

    CIRC_CATEGORIES = [
        ('malabares', _('Juggling')),
        ('trapecio', _('Trapeze')),
        ('clown', _('Clown')),
        ('circo', _('Circus')),
        ('disciplinas_mixtas', _('Mixed disciplines')),
    ]

    id = models.AutoField(primary_key=True)
    item_type = models.CharField(default='show', max_length=10, editable=False)

    name = models.CharField(
        _('Name'),
        max_length=200,
        help_text=_('Event name'),
    )
    image = models.ImageField(
        _('Image'),
        upload_to='shows/images/',
        help_text=_('Promotional image for the event'),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )
    starting_date = models.DateField(
        _('Starting date'),
        default=now,
        help_text=_('Event starting date'),
    )
    end_date = models.DateField(
        _('End date'),
        blank=True,
        null=True,
        help_text=_('Event end date'),
    )
    starting_time = models.TimeField(
        _('Starting time'),
        help_text=_('Event starting time'),
    )
    duration = models.DurationField(
        _('Duration'),
        help_text=_('Duration in HH:MM format (hours:minutes)'),
    )
    max_participants = models.PositiveIntegerField(
        _('Maximum participants'),
        default=100,
    )
    booked_participants = models.PositiveIntegerField(
        _('Booked participants'),
        default=0,
    )
    users_missed_requests = models.PositiveIntegerField(
        _('Missed booking requests'),
        default=0,
    )
    audience = models.CharField(
        _('Audience'),
        max_length=15,
        choices=AUDIENCE_TYPES,
        default='todo_publico',
        help_text=_('Specify whether the event is for children, adults, or all audiences.'),
    )
    price_per_seat_adult = models.DecimalField(
        _('Adult ticket price'),
        max_digits=6,
        decimal_places=2,
        help_text=_('Price per adult ticket'),
    )
    price_per_seat_reduction = models.DecimalField(
        _('Reduced ticket price'),
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Reduced ticket price, where applicable'),
    )
    circ_category = models.CharField(
        _('Circus category'),
        max_length=100,
        choices=CIRC_CATEGORIES,
        default='',
        null=True,
    )

    weekday_1 = models.CharField(
        _('First weekday'),
        max_length=9,
        choices=WEEKDAYS,
    )
    weekday_2 = models.CharField(
        _('Second weekday'),
        max_length=9,
        choices=WEEKDAYS,
        blank=True,
        null=True,
    )
    weekday_3 = models.CharField(
        _('Third weekday'),
        max_length=9,
        choices=WEEKDAYS,
        blank=True,
        null=True,
    )
    weekday_4 = models.CharField(
        _('Fourth weekday'),
        max_length=9,
        choices=WEEKDAYS,
        blank=True,
        null=True,
    )
    weekday_5 = models.CharField(
        _('Fifth weekday'),
        max_length=9,
        choices=WEEKDAYS,
        blank=True,
        null=True,
    )
    weekday_6 = models.CharField(
        _('Sixth weekday'),
        max_length=9,
        choices=WEEKDAYS,
        blank=True,
        null=True,
    )
    weekday_7 = models.CharField(
        _('Seventh weekday'),
        max_length=9,
        choices=WEEKDAYS,
        blank=True,
        null=True,
    )

    # Location
    location_name = models.CharField(
        _('Venue name'),
        max_length=255,
        default='por determinar',
        help_text=_('Name of the venue, theatre or location'),
    )
    location_street = models.CharField(
        _('Address'),
        max_length=255,
        default='por determinar',
        help_text=_('Street address of the venue, theatre or location'),
        null=True,
    )
    location_cp = models.IntegerField(
        _('Postcode'),
        blank=True,
        null=True,
        help_text=_('Venue postcode (optional)'),
    )
    location_city = models.CharField(
        _('City'),
        max_length=255,
        default='por determinar',
        help_text=_('City where the venue is located'),
    )

    def save(self, *args, **kwargs):
        """Save the event while respecting audience-specific pricing logic."""
        if self.audience == 'adultos':
            self.price_per_seat_reduction = None
        super().save(*args, **kwargs)

    def book_participant(self):
        """Book a participant when space is available."""
        if self.booked_participants < self.max_participants:
            self.booked_participants += 1
            self.save()
        else:
            self.users_missed_requests += 1
            self.save()
            raise ValueError(_('This event is fully booked!'))

    def remaining_seats(self):
        return self.max_participants - self.booked_participants

    def get_formatted_duration(self):
        if self.duration:
            total_seconds = self.duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            return f"{hours:02}:{minutes:02}"
        return "00:00"

    def __str__(self):
        return self.name