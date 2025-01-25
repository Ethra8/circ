from django.db import models

from django.utils.timezone import now
from django.core.exceptions import ValidationError
from decimal import Decimal

class Taller(models.Model):
    WEEKDAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # Name of the taller
    description = models.TextField()  # Detailed description of the taller
    starting_date = models.DateField(default=now)  # Starting date of the taller
    starting_time = models.TimeField()  # Starting time of the taller
    end_time = models.TimeField()  # End time of the taller
    duration = models.PositiveIntegerField(help_text="Duration in weeks")  # Duration in weeks
    max_participants = models.PositiveIntegerField()  # Maximum participants allowed
    booked_participants = models.PositiveIntegerField(default=0)  # Booked participants, starts at 0
    users_missed_requests = models.PositiveIntegerField(default=0)  # Track users who couldn't enroll
    price = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('20.00'),
        help_text="Price per seat for adults",
    )
    circ_category = models.CharField(max_length=100)  # Category for the taller
    weekday_1 = models.CharField(max_length=9, choices=WEEKDAYS)  # Mandatory first weekday
    weekday_2 = models.CharField(max_length=9, choices=WEEKDAYS, blank=True, null=True)  # Optional second weekday
    # Location fields
    location_name = models.CharField(
        max_length=255,
        default='por determinar',
        help_text="Name of the location"
    )
    location_street = models.CharField(
        max_length=255,
        default='por determinar',
        help_text="Street address of the location"
    )
    location_cp = models.IntegerField(
        blank=True,
        null=True,
        help_text="Postal code (optional)"
    )
    location_city = models.CharField(
        max_length=255,
        default='por determinar',
        help_text="City where the taller is held"
    )

    def clean(self):
        """
        Validation:
        - End time must be after the starting time.
        - Weekday 1 and Weekday 2 must be different if both are provided.
        """
        if self.end_time <= self.starting_time:
            raise ValidationError("End time must be after the starting time.")
        
        if self.weekday_2 and self.weekday_1 == self.weekday_2:
            raise ValidationError("Weekday 1 and Weekday 2 cannot be the same.")

    def book_participant(self):
        """
        Increments the booked_participants count if there's space available.
        If the taller is fully booked, increments users_missed_requests.
        """
        if self.booked_participants < self.max_participants:
            self.booked_participants += 1
            self.save()
        else:
            self.users_missed_requests += 1
            self.save()
            raise ValueError("This taller is fully booked!")

    def __str__(self):
        return self.name
