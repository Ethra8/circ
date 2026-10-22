from django import forms
from circ.widgets import TranslatedFileInput
from .models import Taller

class TallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = [
            'name',
            'image',
            'description',
            'starting_date',
            'end_date',
            'starting_time',
            'end_time',
            'duration',
            'max_participants',
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
            'image': TranslatedFileInput(),
            'starting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'starting_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }