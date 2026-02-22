# AGENTS.md — AntiGravity Web Platform

Welcome, agent! This file tells you everything you need to know to work on
the AntiGravity project. Read this top to bottom before writing any code.

---

## What This Project Is

AntiGravity is a full-stack web application built with:

- **Backend:** Python + Django
- **Frontend:** Django templates (HTML/CSS/JS — no heavy framework)
- **Database:** PostgreSQL
- **Auth:** Django's built-in auth system, hardened with extra security layers
- **Deployment target:** Linux server (Ubuntu), served via Gunicorn + Nginx

The goal is to keep every file readable and editable by an average human.
That means: clear variable names, short functions, plain comments, and no
clever one-liners that require a PhD to decipher.

---

## Project Structure

```
antigravity/
│
├── manage.py                  # Django entry point — run commands from here
├── requirements.txt           # All Python dependencies listed here
├── .env                       # Secret keys and config — never commit this file
├── .env.example               # Safe template showing what .env needs
│
├── config/                    # Project-level Django settings and URL routing
│   ├── settings/
│   │   ├── base.py            # Settings shared across all environments
│   │   ├── development.py     # Settings only for local development
│   │   └── production.py      # Settings only for live server
│   ├── urls.py                # Top-level URL routes
│   └── wsgi.py                # Web server entry point
│
├── apps/                      # All Django apps live here
│   ├── core/                  # Shared utilities, base models, middleware
│   ├── accounts/              # User registration, login, logout, profile
│   ├── dashboard/             # Main user dashboard after login
│   └── api/                   # Any JSON endpoints (optional, REST-style)
│
├── templates/                 # All HTML files
│   ├── base.html              # The main layout every page extends
│   ├── accounts/              # Login, signup, password reset pages
│   └── dashboard/             # Dashboard pages
│
├── static/                    # CSS, JS, images (your own files)
│   ├── css/
│   ├── js/
│   └── images/
│
└── media/                     # User-uploaded files (not committed to git)
```

---

## Dev Environment Setup

Follow these steps in order. Do not skip any.

### 1. Clone and enter the project

```bash
git clone <repo-url> antigravity
cd antigravity
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

Always activate the virtual environment before running any commands.
If you see `(venv)` at the start of your terminal prompt, you're in.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

```bash
cp .env.example .env
```

Then open `.env` and fill in the values. Every key in `.env.example` must
have a real value in `.env` before the app will start.

### 5. Set up the database

```bash
python manage.py migrate
python manage.py createsuperuser   # Follow the prompts to create an admin user
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open your browser and go to: http://127.0.0.1:8000

Admin panel is at: http://127.0.0.1:8000/admin

---

## How to Add a New Feature

This is the standard pattern. Follow it every time.

1. Figure out which app the feature belongs to (or create a new app under `apps/`).
2. Add or edit the **model** in `apps/<appname>/models.py` — this is your database table.
3. Run `python manage.py makemigrations` then `python manage.py migrate` to update the DB.
4. Add the **view** in `apps/<appname>/views.py` — this handles the request and response.
5. Add the **URL** in `apps/<appname>/urls.py`, then wire it into `config/urls.py`.
6. Add the **template** in `templates/<appname>/`.
7. Write a **test** in `apps/<appname>/tests.py`.
8. Run the tests and make sure everything passes before committing.

---

## Code Style Rules

These rules exist so any human can read and edit the code.

### Naming

- Variables and functions: `snake_case` — e.g., `user_profile`, `get_active_users()`
- Classes: `PascalCase` — e.g., `UserProfile`, `DashboardView`
- Constants: `ALL_CAPS` — e.g., `MAX_LOGIN_ATTEMPTS = 5`
- URL names: `kebab-case` — e.g., `user-profile`, `password-reset`
- Template names: `snake_case.html` — e.g., `user_profile.html`

### Function length

Keep functions short. If a function is longer than 30 lines, split it up.
Each function should do one thing and do it well.

### Comments

Write comments that explain **why**, not **what**. The code shows what.
The comment should explain the reason behind a decision.

```python
# Good comment
# We check the rate limit before anything else so we don't
# waste database calls on requests that are clearly abusive.
if is_rate_limited(request):
    return HttpResponseTooManyRequests()

# Bad comment — just restates the code
# Check if rate limited
if is_rate_limited(request):
    return HttpResponseTooManyRequests()
```

### No magic numbers

If you use a number, give it a name.

```python
# Bad
if login_attempts > 5:
    lock_account(user)

# Good
MAX_LOGIN_ATTEMPTS = 5
if login_attempts > MAX_LOGIN_ATTEMPTS:
    lock_account(user)
```

---

## Security Rules

Security is not optional. Every one of these must be in place.

### Environment and Secrets

- `SECRET_KEY`, database passwords, API keys — all go in `.env`, never in code.
- Never commit `.env` to git. It is in `.gitignore` already. Do not remove it.
- Use `python-decouple` or `django-environ` to read `.env` values in settings.

```python
# config/settings/base.py — correct way to read secrets
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DATABASE_URL = config('DATABASE_URL')
```

### Django Security Settings

These must be set to `True` in `production.py`. Do not change them to `False`.

```python
DEBUG = False                      # Never True in production
SECURE_BROWSER_XSS_FILTER = True   # Tells browsers to block XSS attacks
SECURE_CONTENT_TYPE_NOSNIFF = True # Stops browsers from guessing file types
X_FRAME_OPTIONS = 'DENY'           # Prevents your pages being embedded in iframes
SECURE_SSL_REDIRECT = True         # Forces all traffic to use HTTPS
SESSION_COOKIE_SECURE = True       # Session cookie only sent over HTTPS
CSRF_COOKIE_SECURE = True          # CSRF cookie only sent over HTTPS
SECURE_HSTS_SECONDS = 31536000     # Tells browsers to always use HTTPS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
ALLOWED_HOSTS = ['yourdomain.com'] # Only allow your real domain — not '*'
```

### CSRF Protection

Django's CSRF protection is on by default. Do not disable it. Every HTML
form must include `{% csrf_token %}` inside the `<form>` tag.

```html
<form method="post" action="{% url 'accounts:login' %}">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Log in</button>
</form>
```

### SQL Injection

Always use Django's ORM or parameterized queries. Never build SQL strings
with user input.

```python
# Bad — never do this
User.objects.raw(f"SELECT * FROM users WHERE name = '{name}'")

# Good — the ORM handles escaping automatically
User.objects.filter(name=name)
```

### Authentication and Passwords

- Use Django's built-in `authenticate()` and `login()` — do not roll your own.
- Passwords are automatically hashed by Django. Never store plain-text passwords.
- Enforce a strong password policy using `django-password-validators`.
- Add rate limiting on login: lock the account after `MAX_LOGIN_ATTEMPTS` failures.

```python
# apps/accounts/views.py — login rate limiting example
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

def login_view(request):
    attempts = request.session.get('login_attempts', 0)

    if attempts >= MAX_LOGIN_ATTEMPTS:
        # Tell the user their account is temporarily locked
        return render(request, 'accounts/locked.html')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            request.session['login_attempts'] = 0   # Reset on success
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:home')
        else:
            request.session['login_attempts'] = attempts + 1
    ...
```

### Access Control

Every view that requires a logged-in user must be protected. Use Django's
built-in decorator or mixin.

```python
# Function-based views — use the decorator
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    ...

# Class-based views — use the mixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class DashboardView(LoginRequiredMixin, View):
    ...
```

Never assume a user is allowed to see something just because they are logged in.
Check that they own the object or have the right permission.

```python
# Good — confirm the user owns this item before showing it
item = get_object_or_404(Item, pk=item_id, owner=request.user)

# Bad — anyone logged in can see anyone's item
item = get_object_or_404(Item, pk=item_id)
```

### File Uploads

If the app accepts file uploads from users:

- Validate the file type by checking its actual content, not just the extension.
- Store uploaded files in `media/` which is outside the web root if possible.
- Never execute or import uploaded files.
- Set a reasonable file size limit.

```python
# apps/core/validators.py
from django.core.exceptions import ValidationError

MAX_UPLOAD_SIZE_MB = 5

def validate_file_size(file):
    limit = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file.size > limit:
        raise ValidationError(f'File must be smaller than {MAX_UPLOAD_SIZE_MB}MB.')
```

### Logging

Log security-relevant events so you can investigate issues later.
Never log passwords or full session tokens.

```python
import logging
logger = logging.getLogger(__name__)

# Log failed logins (useful for spotting attacks)
logger.warning('Failed login attempt for email: %s from IP: %s', email, ip_address)

# Log successful logins
logger.info('User %s logged in successfully.', user.id)
```

---

## Testing Instructions

Every new feature needs tests. Tests go in `apps/<appname>/tests.py`.

### Run all tests

```bash
python manage.py test
```

### Run tests for one app only

```bash
python manage.py test apps.accounts
```

### Run one specific test

```bash
python manage.py test apps.accounts.tests.LoginViewTest.test_locked_after_five_attempts
```

### What to test

- Happy path: the normal expected flow works.
- Sad path: invalid input is rejected gracefully.
- Security: a logged-out user cannot reach protected pages. A user cannot
  access another user's data.

```python
# apps/accounts/tests.py — example security test
from django.test import TestCase
from django.urls import reverse

class DashboardAccessTest(TestCase):

    def test_logged_out_user_is_redirected(self):
        # A user who is not logged in should be sent to the login page
        response = self.client.get(reverse('dashboard:home'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_logged_in_user_can_access_dashboard(self):
        user = User.objects.create_user(username='jane', password='Secur3Pass!')
        self.client.login(username='jane', password='Secur3Pass!')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
```

All tests must pass before you open a pull request. If a test is failing and
you do not know why, ask — do not delete the test.

---

## Database Rules

- Never delete a migration file. If a migration has a mistake, create a new
  migration to fix it.
- Do not edit a migration file by hand unless absolutely necessary, and add
  a comment explaining why if you do.
- Every model should have a `__str__` method so it shows a useful name in
  the Django admin.
- Add `db_index=True` to fields you filter or search by frequently.

```python
# apps/accounts/models.py — clean, readable model example
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extra information attached to a user account."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Shows "Profile of jane" in the admin panel
        return f'Profile of {self.user.username}'
```

---

## Templates and Frontend

- Keep logic out of templates. Templates should only display data, not
  calculate it. If you need to compute something, do it in the view.
- Use `{% url 'app:name' %}` for all links — never hardcode paths.
- Every page extends `base.html`.

```html
<!-- templates/dashboard/home.html -->
{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}

{% block content %}
  <h1>Welcome, {{ user.username }}</h1>
  <a href="{% url 'accounts:logout' %}">Log out</a>
{% endblock %}
```

- CSS and JS go in `static/`. Reference them with `{% static %}`.
- Do not put `<style>` or `<script>` blocks inline in templates unless it is
  a tiny one-liner. Put them in the proper static files.

---

## Git and Pull Request Instructions

### Branch naming

```
feature/short-description
bugfix/short-description
security/short-description
```

### Commit messages

Write in plain English, past tense, short and direct.

```
# Good
Added rate limiting to login view
Fixed password reset email not sending in production
Removed hardcoded secret key from settings

# Bad
fix
wip
changes
```

### Before opening a pull request

Run all of these and make sure they pass:

```bash
python manage.py test          # All tests must pass
python manage.py check         # Django's built-in security and config checks
python manage.py check --deploy  # Extra checks for production readiness
```

### PR description

Include:
1. What changed and why
2. How to test it manually
3. Any migration that needs to run

---

## Common Commands Reference

| What you want to do | Command |
|---|---|
| Start the dev server | `python manage.py runserver` |
| Create DB migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Create a superuser | `python manage.py createsuperuser` |
| Open Django shell | `python manage.py shell` |
| Run all tests | `python manage.py test` |
| Check for config issues | `python manage.py check` |
| Collect static files | `python manage.py collectstatic` |
| See all URL routes | `python manage.py show_urls` |

---

## Things You Must Never Do

- Never set `DEBUG = True` on the production server.
- Never commit `.env` or any file containing passwords or secret keys.
- Never use `*` in `ALLOWED_HOSTS` on the production server.
- Never disable CSRF protection.
- Never store passwords in plain text.
- Never use `eval()` or `exec()` with user input.
- Never suppress an exception with a bare `except:` — catch specific errors.
- Never delete a migration file.
- Never push code that makes tests fail.

---

*This file is for both humans and agents. Keep it up to date as the project grows.*
