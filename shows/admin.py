from django.contrib import admin
from .models import Show

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'time', 'total_seats', 'remaining_seats', 'price_per_seat_adult', 'price_per_seat_reduction')