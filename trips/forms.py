from django import forms
from .models import Trip
from django.utils import timezone

class TripForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select the start date of your trip'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select the end date of your trip'
    )
    image = forms.ImageField(required=False, help_text='Upload an image for your trip')

    class Meta:
        model = Trip
        fields = ['destination', 'start_date', 'end_date', 'description', 'image']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past.")
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before start date.")

        return cleaned_data

class TripSearchForm(forms.Form):
    destination = forms.CharField(required=False)
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
