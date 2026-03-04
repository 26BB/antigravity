"""
apps/accounts/views.py

Security features baked in:
- @axes_dispatch on login: auto-lockout after 5 failed attempts
- @ratelimit on register and password-reset: max 10 requests/min per IP
- All sensitive events logged for security auditing
"""

import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from axes.decorators import axes_dispatch
from django_ratelimit.decorators import ratelimit

logger = logging.getLogger(__name__)

MAX_LOGIN_ATTEMPTS = 5  # Must match AXES_FAILURE_LIMIT in settings


@axes_dispatch   # Tracks failures; locks account after MAX_LOGIN_ATTEMPTS
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Secure login with brute-force protection via django-axes."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Log success for auditing — never log the password
            logger.info('User %s logged in successfully from IP %s.',
                        user.id, _get_client_ip(request))
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        else:
            logger.warning('Failed login attempt for username "%s" from IP %s.',
                           request.POST.get('username', ''), _get_client_ip(request))
    else:
        form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {'form': form})


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration with IP-based rate limiting (max 10 attempts/min)."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info('New user registered: ID %s from IP %s.',
                        user.id, _get_client_ip(request))
            messages.success(request, 'Account created! Welcome aboard.')
            return redirect('dashboard:home')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["POST"])
def logout_view(request):
    """Log out via POST only — prevents logout CSRF attacks."""
    logger.info('User %s logged out.', request.user.id if request.user.is_authenticated else 'anon')
    logout(request)
    return redirect('accounts:login')


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@require_http_methods(["GET", "POST"])
def password_reset_view(request):
    """Password reset with rate limiting — prevents email enumeration spam."""
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # Always show the same message whether the email exists or not
        # This prevents user enumeration attacks
        form.save(request=request)
        messages.info(request, 'If that email is registered, you will receive a reset link shortly.')
        return redirect('accounts:login')
    return render(request, 'accounts/password_reset.html', {'form': form})


def locked_view(request):
    """Shown when an account is locked by django-axes after too many failures."""
    return render(request, 'accounts/locked.html', status=403)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _get_client_ip(request):
    """Extract the real client IP, accounting for proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')
