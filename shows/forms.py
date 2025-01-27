from django import forms
from datetime import timedelta
from .models import Show


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = [
            'name',
            'image',
            'description',
            'starting_date',
            'end_date',
            'starting_time',
            'duration',
            'max_participants',
            'booked_participants',
            'audience',
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
            'starting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'starting_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'audience': forms.Select(attrs={'class': 'form-control'}),
            'circ_category': forms.Select(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'booked_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'weekday_1': forms.Select(attrs={'class': 'form-control'}),
            'weekday_2': forms.Select(attrs={'class': 'form-control'}),
            'location_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location_street': forms.TextInput(attrs={'class': 'form-control'}),
            'location_cp': forms.NumberInput(attrs={'class': 'form-control'}),
            'location_city': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide irrelevant pricing fields based on the audience
        audience = self.instance.audience if self.instance else None
        if audience == 'adultos':
            self.fields['price_per_seat_reduction'].widget = forms.HiddenInput()
            self.fields['price_per_seat_reduction'].required = False
        elif audience == 'niños':
            self.fields['price_per_seat_adult'].widget = forms.HiddenInput()
            self.fields['price_per_seat_adult'].required = False

    def clean(self):
        """
        Custom validation for pricing fields and duration.
        """
        cleaned_data = super().clean()
        audience = cleaned_data.get('audience')
        price_per_seat_adult = cleaned_data.get('price_per_seat_adult')
        price_per_seat_reduction = cleaned_data.get('price_per_seat_reduction')
        duration = cleaned_data.get('duration')

        # Validate pricing fields based on audience
        if audience == 'adultos' and not price_per_seat_adult:
            self.add_error('price_per_seat_adult', "Price per seat for adults is required when audience is 'adultos'.")
        if audience == 'niños' and not price_per_seat_reduction:
            self.add_error('price_per_seat_reduction', "Price per seat for children is required when audience is 'niños'.")

        # Validate duration format (only HH:MM is allowed)
        if duration:
            try:
                total_seconds = duration.total_seconds()
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                if seconds != 0:
                    raise forms.ValidationError("Duration should only include hours and minutes (seconds must be 00).")
            except AttributeError:
                raise forms.ValidationError("Invalid duration format. Please use HH:MM:00")

        return cleaned_data
