from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'phone_number', 'license_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Admins shouldn't be created via standard sign up
        self.fields['role'].choices = [c for c in User.ROLE_CHOICES if c[0] != 'admin']
