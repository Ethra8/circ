from django.db import models

class Show(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the show")
    location = models.CharField(max_length=200, help_text="Location of the show")
    time = models.DateTimeField(help_text="Date and time of the show")
    duration = models.DurationField(help_text="Duration of the show (HH:MM:SS)")
    image = models.ImageField(upload_to='shows/images/', help_text="Image representing the show", blank=True, null=True)
    total_seats = models.PositiveIntegerField(help_text="Total number of seats available")
    remaining_seats = models.PositiveIntegerField(help_text="Number of seats still available")

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

