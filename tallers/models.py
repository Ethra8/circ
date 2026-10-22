from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Taller(models.Model):

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
    item_type = models.CharField(default='taller', max_length=10, editable=False)

    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('Workshop name'),
    )

    image = models.ImageField(
        _('Image'),
        upload_to='tallers/images/',
        help_text=_('Promotional image for the workshop'),
        blank=True,
        null=True,
    )

    description = models.TextField(
        _('Description'),
        help_text=_('Detailed description of the workshop'),
    )

    starting_date = models.DateField(
        _('Starting date'),
        default=now,
        help_text=_('Workshop starting date'),
    )

    end_date = models.DateField(
        _('End date'),
        blank=True,
        null=True,
        help_text=_('Workshop end date'),
    )

    starting_time = models.TimeField(
        _('Starting time'),
        help_text=_('Workshop starting time'),
    )

    end_time = models.TimeField(
        _('End time'),
        help_text=_('Workshop end time'),
    )

    duration = models.PositiveIntegerField(
        _('Duration'),
        help_text=_('Duration in weeks'),
    )

    max_participants = models.PositiveIntegerField(
        _('Maximum participants'),
        help_text=_('Maximum number of available places'),
    )

    booked_participants = models.PositiveIntegerField(
        _('Booked participants'),
        default=0,
        help_text=_('Number of places already booked'),
    )

    users_missed_requests = models.PositiveIntegerField(
        _('Missed booking requests'),
        default=0,
        help_text=_('Number of users who requested a place after the workshop became full'),
    )

    audience = models.CharField(
        _('Audience'),
        max_length=15,
        choices=AUDIENCE_TYPES,
        default='todo_publico',
        help_text=_('Specify whether the workshop is for children, adults, or all audiences.'),
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
        help_text=_('Choose the circus category for the workshop'),
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
        help_text=_('Name of the venue, theatre or location where the workshop takes place'),
    )

    location_street = models.CharField(
        _('Address'),
        max_length=255,
        default='por determinar',
        help_text=_('Street address of the venue, theatre or location'),
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
        help_text=_('City where the workshop takes place'),
    )

    def clean(self):
        """
        Validate workshop times, weekdays and audience-specific pricing.
        """
        if self.end_time and self.starting_time and self.end_time <= self.starting_time:
            raise ValidationError(
                _('End time must be after the starting time.')
            )

        if self.weekday_2 and self.weekday_1 == self.weekday_2:
            raise ValidationError(
                _('First weekday and second weekday cannot be the same.')
            )

        if self.audience == 'adultos' and self.price_per_seat_reduction:
            raise ValidationError(
                _('Reduced ticket price must not be set for an adults-only workshop.')
            )

    def save(self, *args, **kwargs):
        """
        Save the workshop while respecting audience-specific pricing logic.
        """
        if self.audience == 'adultos':
            self.price_per_seat_reduction = None

        super().save(*args, **kwargs)

    def book_participant(self):
        """
        Book a participant when space is available.
        """
        if self.booked_participants < self.max_participants:
            self.booked_participants += 1
            self.save()
        else:
            self.users_missed_requests += 1
            self.save()
            raise ValueError(
                _('This workshop is fully booked!')
            )

    def remaining_seats(self):
        return self.max_participants - self.booked_participants

    def __str__(self):
        return self.name