"""Core app — shared utilities, home redirect."""

from django.shortcuts import redirect
from django.urls import path

app_name = 'core'


def home_redirect(request):
    """Redirect root URL to dashboard (or login if not authenticated)."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return redirect('accounts:login')


urlpatterns = [
    path('', home_redirect, name='home'),
]
