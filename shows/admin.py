from django.contrib import admin
from .models import Show

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'time', 'total_seats', 'remaining_seats')