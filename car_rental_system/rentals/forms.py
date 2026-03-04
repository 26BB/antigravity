from django import forms
from .models import Booking, TripLog

class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'purpose']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TripLogForm(forms.ModelForm):
    class Meta:
        model = TripLog
        fields = ['start_odometer', 'end_odometer', 'driver_feedback']
