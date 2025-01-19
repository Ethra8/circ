from django import forms
from .models import Show

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = [
            'name', 'description', 'location', 'time', 'duration', 'image',
            'total_seats', 'remaining_seats', 'price_per_seat_adult', 'price_per_seat_reduction'
        ]
