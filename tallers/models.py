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
    item_type = models.CharField(default='taller', max_length=10, editable=False)
    name = models.CharField(max_length=255)  # Name of the taller
    image = models.ImageField(
        upload_to='tallers/images/', 
        help_text="Image de promoción del taller", 
        blank=True, 
        null=True
    )
    description = models.TextField()  # Detailed description of the taller
    starting_date = models.DateField(default=now, help_text="Fecha de inicio del taller")  # Starting date of the taller
    end_date = models.DateField(blank=True, null=True, help_text="Fecha de finalización del taller")
    starting_time = models.TimeField(help_text="Hora de inicio del taller")  # Starting time of the taller
    end_time = models.TimeField(help_text="Hora de fin del taller")  # End time of the taller
    duration = models.PositiveIntegerField(help_text="Duración en semanas")  # Duration in weeks
    max_participants = models.PositiveIntegerField(help_text="Máximas plazas")  # Maximum participants allowed
    booked_participants = models.PositiveIntegerField(default=0, help_text="Plazas ocupadas (reservada)")  # Booked participants, starts at 0
    users_missed_requests = models.PositiveIntegerField(default=0, help_text="Usuarios que han pedido tener plaza, una vez agotadas - ¿Interesa repetir evento?")  # Track users who couldn't enroll
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
        help_text="Categoría de circo del taller"
    ) 
    weekday_1 = models.CharField(max_length=9, choices=WEEKDAYS, help_text="Día de la semana en el que desarrola el taller (1º es obligatorio)")  # Mandatory first weekday
    weekday_2 = models.CharField(max_length=9, choices=WEEKDAYS, blank=True, null=True, help_text="Día de la semana en el que desarrola el taller (2º es opcional)") 
    # Location fields
    location_name = models.CharField(
        max_length=255,
        default='por determinar',
        help_text="Nombre del lugar/local/teatro donde se desarrolla el taller"
    )
    location_street = models.CharField(
        max_length=255,
        default='por determinar',
        help_text="Dirección del local/teatro/lugar"
    )
    location_cp = models.IntegerField(
        blank=True,
        null=True,
        help_text="Código postal del local/teatro/lugar (opcional)"
    )
    location_city = models.CharField(
        max_length=255,
        default='por determinar',
        help_text="Ciudad donde se desarrolla el taller"
    )

    def clean(self):
        """
        Validation:
        - End time must be after the starting time.
        - Weekday 1 and Weekday 2 must be different if both are provided.
        - Automatically set price_per_seat_reduction to 0 if the audience is 'adults'.
        """
        if self.end_time <= self.starting_time:
            raise ValidationError("End time must be after the starting time.")
        
        if self.weekday_2 and self.weekday_1 == self.weekday_2:
            raise ValidationError("Weekday 1 and Weekday 2 cannot be the same.")

        if self.audience == 'adultos' and self.price_per_seat_reduction:
            raise ValidationError("price_per_seat_reduction must not be set for audience='adultos'.")

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
            raise ValueError("Este taller está completo!")

    def __str__(self):
        return self.name
