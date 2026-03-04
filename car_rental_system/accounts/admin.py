from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Car Rental Roles', {'fields': ('role', 'phone_number', 'department')}),
        ('Driver Details', {'fields': ('license_number', 'license_expiry')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'role']
    list_filter = ['role', 'is_staff', 'is_active']

admin.site.register(User, CustomUserAdmin)
