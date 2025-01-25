from django.db import models

from django.utils.timezone import now
from django.core.exceptions import ValidationError
from decimal import Decimal

class Show(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=200, help_text="Nombre del Evento")
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, help_text="Local del Evento")
    time = models.DateTimeField(help_text="Fecha y hora del evento")
    duration = models.DurationField(help_text="Duración del evento (HH:MM:SS)")
    image = models.ImageField(upload_to='shows/images/', help_text="Image de promoción del evento", blank=True, null=True)
    total_seats = models.PositiveIntegerField(help_text="Máximo de plazas disponibles")
    remaining_seats = models.PositiveIntegerField(help_text="Número de plazas disponibles")
    price_per_seat_adult = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('20.00'),
        help_text="Precio por ticket adulto",
    )
    price_per_seat_reduction = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('15.00'),
        help_text="Precio por ticket reducido"
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
            raise ValueError("No quedan suficientes plazas")


class Taller(models.Model):
    WEEKDAYS = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # Name of the taller
    description = models.TextField()  # Detailed description of the taller
    starting_date = models.DateField(default=now)  # Starting date of the taller
    starting_time = models.TimeField()  # Starting time of the taller
    end_time = models.TimeField()  # End time of the taller
    duration = models.PositiveIntegerField(help_text="Duración en semanas")  # Duration in weeks
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
            raise ValidationError("El tiempo de acabado tiene que ser superior al tiempo de inicio.")
        
        if self.weekday_2 and self.weekday_1 == self.weekday_2:
            raise ValidationError("Dia 1 y Dia 2 no pueden ser el mismo.")

    def book_participant(self):
        """
        Increments the booked_participants count if there's space available.
        """
        if self.booked_participants < self.max_participants:
            self.booked_participants += 1
            self.save()
        else:
            raise ValueError("Este evento está completo!")

    def __str__(self):
        return self.name