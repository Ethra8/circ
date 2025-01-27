from django.contrib import admin

from datetime import datetime, timedelta

from .models import Show
from .forms import ShowForm

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'audience',
        'starting_date',
        'end_date',
        'starting_time',
        'get_end_time',  # Use a method to calculate end_time dynamically
        'duration_display',
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
                'end_date',
                'duration_display',
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


    def get_end_time(self, obj):
        """
        Dynamically calculate end_time based on starting_time and duration.
        Handles cases where duration is already a timedelta or an integer (minutes).
        """
        if obj.starting_time and obj.duration:
            # Create a temporary datetime object using the current date and starting_time
            starting_datetime = datetime.combine(datetime.today(), obj.starting_time)
            
            # Check if duration is already a timedelta
            if isinstance(obj.duration, timedelta):
                calculated_end_datetime = starting_datetime + obj.duration
            else:
                # Assume duration is an integer representing minutes
                calculated_end_datetime = starting_datetime + timedelta(minutes=obj.duration)
            
            # Extract the time part from the resulting datetime
            return calculated_end_datetime.time().strftime("%H:%M:%S")
        
        return None    
    get_end_time.short_description = "End Time"

    def duration_display(self, obj):
        """Display duration in HH:MM format."""
        total_seconds = obj.duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours:02}:{minutes:02}"

    duration_display.short_description = "Duración (HH:MM)"

    def save_model(self, request, obj, form, change):
        """
        Custom save behavior for the Show model in the admin:
        - Set `price_per_seat_reduction` to 0 if the audience is 'adultos'.
        """
        if obj.audience == 'adultos':
            obj.price_per_seat_reduction = 0
        super().save_model(request, obj, form, change)
