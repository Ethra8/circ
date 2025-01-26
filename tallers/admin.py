from django.contrib import admin
from .models import Taller

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Taller model.
    """
    list_display = (
        'name', 
        'audience', 
        'starting_date', 
        'duration', 
        'price_per_seat_adult', 
        'price_per_seat_reduction', 
        'max_participants', 
        'booked_participants',
        'circ_category',
    )
    list_filter = (
        'audience', 
        'starting_date', 
        'circ_category',
    )
    search_fields = (
        'name', 
        'description', 
        'circ_category',
    )
    readonly_fields = (
        'booked_participants', 
        'users_missed_requests',
    )
    fieldsets = (
        (None, {
            'fields': (
                'name', 
                'description', 
                'image', 
                'circ_category',
            ),
        }),
        ('Audience and Pricing', {
            'fields': (
                'audience', 
                'price_per_seat_adult', 
                'price_per_seat_reduction',
            ),
        }),
        ('Schedule', {
            'fields': (
                'starting_date', 
                'starting_time', 
                'end_time', 
                'duration',
            ),
        }),
        ('Participants', {
            'fields': (
                'max_participants', 
                'booked_participants', 
                'users_missed_requests',
            ),
        }),
        ('Location', {
            'fields': (
                'location_name', 
                'location_street', 
                'location_cp', 
                'location_city',
            ),
        }),
        ('Weekdays', {
            'fields': (
                'weekday_1', 
                'weekday_2',
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Custom save behavior for the Taller model in the admin:
        - Set `price_per_seat_reduction` to 0 if the audience is 'adultos'.
        """
        if obj.audience == 'adultos':
            obj.price_per_seat_reduction = 0
        super().save_model(request, obj, form, change)
