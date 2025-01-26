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
            'price', 
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
        }
        help_texts = {
            'booked_participants': 'Number of participants already booked.',
            'duration': 'Duration in weeks.',
            'weekday_1': 'Select the primary weekday for the session.',
            'weekday_2': 'Optional: Select a second weekday.',
        }

    def clean(self):
        """
        Add custom validation for the form fields.
        """
        cleaned_data = super().clean()
        starting_time = cleaned_data.get('starting_time')
        end_time = cleaned_data.get('end_time')
        weekday_1 = cleaned_data.get('weekday_1')
        weekday_2 = cleaned_data.get('weekday_2')

        # Validation: End time must be after starting time
        if starting_time and end_time and end_time <= starting_time:
            self.add_error('end_time', "End time must be after starting time.")

        # Validation: Weekday 1 and Weekday 2 must not be the same
        if weekday_1 and weekday_2 and weekday_1 == weekday_2:
            self.add_error('weekday_2', "Weekday 2 must be different from Weekday 1.")

        return cleaned_data
