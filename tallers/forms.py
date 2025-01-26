from django import forms
from .models import Taller

class TallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = [
            'name',
            'image',
            'description', 
            'starting_date', 
            'starting_time', 
            'end_time', 
            'duration', 
            'max_participants', 
            'booked_participants', 
            'audience',  # Include audience
            'price_per_seat_adult',
            'price_per_seat_reduction',
            'circ_category', 
            'weekday_1', 
            'weekday_2', 
            'location_name', 
            'location_street', 
            'location_cp', 
            'location_city',
        ]
        widgets = {
            'starting_date': forms.DateInput(attrs={'type': 'date'}),
            'starting_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'audience': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for audience
        }
        help_texts = {
            'audience': 'Specify whether the taller is for children, adults, or both.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.audience == 'adultos':
            self.fields['price_per_seat_reduction'].widget = forms.HiddenInput()
            self.fields['price_per_seat_reduction'].required = False
        elif self.instance and self.instance.audience == 'niños':
            self.fields['price_per_seat_adult'].widget = forms.HiddenInput()
            self.fields['price_per_seat_adult'].required = False

    def clean(self):
        """
        Add custom validation to ensure appropriate pricing fields are filled based on the audience.
        """
        cleaned_data = super().clean()
        audience = cleaned_data.get('audience')

        if audience == 'adultos' and not cleaned_data.get('price_per_seat_adult'):
            self.add_error('price_per_seat_adult', "Price per seat for adults is required when audience is 'adultos'.")

        if audience == 'niños' and not cleaned_data.get('price_per_seat_reduction'):
            self.add_error('price_per_seat_reduction', "Price per seat for children is required when audience is 'niños'.")

        return cleaned_data
