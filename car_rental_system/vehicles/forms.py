from django import forms
from .models import Vehicle, VehicleAvailability

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'license_plate', 'insurance_provider', 'insurance_policy_number', 'insurance_expiry']

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = VehicleAvailability
        fields = ['day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
