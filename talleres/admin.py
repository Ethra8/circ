from django.contrib import admin
from .models import Taller

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'starting_date', 
        'max_participants', 
        'booked_participants', 
        'users_missed_requests',
    )  # Columns displayed in the admin list view
    list_filter = ('circ_category', 'starting_date')  # Add filters for admin
    search_fields = ('name', 'description', 'location_name', 'location_city')  # Add search fields
    readonly_fields = ('users_missed_requests',)  # Prevent manual editing of missed requests

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'circ_category')
        }),
        ('Schedule', {
            'fields': ('starting_date', 'starting_time', 'end_time', 'duration', 'weekday_1', 'weekday_2')
        }),
        ('Location', {
            'fields': ('location_name', 'location_street', 'location_cp', 'location_city')
        }),
        ('Participants', {
            'fields': ('max_participants', 'booked_participants', 'users_missed_requests'),
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
    )
