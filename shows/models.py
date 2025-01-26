from django.db import models

from django.utils.timezone import now
from django.core.exceptions import ValidationError
from decimal import Decimal

class Show(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    item_type = models.CharField(default='show', max_length=10, editable=False)
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
