from django.db import models

from django.utils.timezone import now
from django.core.exceptions import ValidationError
from decimal import Decimal

class Show(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=200, help_text="Name of the show")
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, help_text="Location of the show")
    time = models.DateTimeField(help_text="Date and time of the show")
    duration = models.DurationField(help_text="Duration of the show (HH:MM:SS)")
    image = models.ImageField(upload_to='shows/images/', help_text="Image representing the show", blank=True, null=True)
    total_seats = models.PositiveIntegerField(help_text="Total number of seats available")
    remaining_seats = models.PositiveIntegerField(help_text="Number of seats still available")
    price_per_seat_adult = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('20.00'),
        help_text="Price per seat for adults",
    )
    price_per_seat_reduction = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('15.00'),
        help_text="Price per seat with a reduction"
    )

    def __str__(self):
        return f"{self.name} - {self.location}"

    def book_seats(self, number_of_seats):
        """
        Book a number of seats if available.
        """
        if number_of_seats <= self.remaining_seats:
            self.remaining_seats -= number_of_seats
            self.save()
        else:
            raise ValueError("Not enough seats available")


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
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the taller
    circ_category = models.CharField(max_length=100)  # Category for the taller
    weekday_1 = models.CharField(max_length=9, choices=WEEKDAYS)  # Mandatory first weekday
    weekday_2 = models.CharField(max_length=9, choices=WEEKDAYS, blank=True, null=True)  # Optional second weekday

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
        """
        if self.booked_participants < self.max_participants:
            self.booked_participants += 1
            self.save()
        else:
            raise ValueError("This taller is fully booked!")

    def __str__(self):
        return self.name