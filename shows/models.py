from django.db import models

from django.utils.timezone import now
from django.core.exceptions import ValidationError
from decimal import Decimal

class Show(models.Model):
    WEEKDAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    AUDIENCE_TYPES = [
        ('niños', 'Niños'),
        ('adultos', 'Adultos'),
        ('todo_publico', 'Todo Público'),
    ]

    CIRC_CATEGORIES = [
        ('malabares', 'Malabares'),
        ('trapecio', 'Trapecio'),
        ('clown', 'Clown (Payaso)'),
        ('cuerda_floja', 'Cuerda Floja'),
    ]

    id = models.AutoField(primary_key=True)
    item_type = models.CharField(default='show', max_length=10, editable=False)
    name = models.CharField(max_length=200, help_text="Nombre del Evento")
    image = models.ImageField(upload_to='shows/images/', help_text="Image de promoción del evento", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    starting_date = models.DateField(default=now, help_text="Fecha de inicio")  # Starting date of the taller
    end_date = models.DateField(blank=True, null=True, help_text="Fecha de finalización del evento")
    starting_time = models.TimeField(help_text="Hora de inicio")  # Starting time of the taller
    duration = models.DurationField(help_text="Duración del evento (HH:MM:SS)")
    max_participants = models.PositiveIntegerField(default=100)  # Maximum participants allowed
    booked_participants = models.PositiveIntegerField(default=0)  # Booked participants, starts at 0
    users_missed_requests = models.PositiveIntegerField(default=0)  # Track users who couldn't enroll
    audience = models.CharField(
    max_length=15,
    choices=AUDIENCE_TYPES,
    default='todo_publico',
    help_text="Especifique si el taller es para niños, adultos, o todo público."
    )
    price_per_seat_adult = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        help_text="Precio por ticket adulto",
    )
    price_per_seat_reduction = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Precio por ticket reducido (solo para niños)"
    )
    circ_category = models.CharField(
        max_length=100,
        choices=CIRC_CATEGORIES,
        default='',
        null=True,
    ) 
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
        help_text="Street address of the location",
        null=True
    )
    location_cp = models.IntegerField(
        blank=True,
        null=True,
        help_text="Postal code (optional)",
    )
    location_city = models.CharField(
        max_length=255,
        default='por determinar',
        help_text="City where the taller is held"
    )


    def save(self, *args, **kwargs):
        """
        Save the Taller instance while respecting audience-specific logic.
        """
        if self.audience == 'adultos':
            self.price_per_seat_reduction = None  # Ignore this field for adultos
        super().save(*args, **kwargs)


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
            raise ValueError("Este evento está completo!")

    def __str__(self):
        return self.name
