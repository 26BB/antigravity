from django.contrib import admin
from .models import RentalPolicy, Booking, TripLog

@admin.register(RentalPolicy)
class RentalPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'hourly_rate', 'per_km_rate', 'is_active', 'created_at')
    list_filter = ('is_active',)

class TripLogInline(admin.StackedInline):
    model = TripLog
    can_delete = False

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('driver__username', 'vehicle__license_plate')
    inlines = [TripLogInline]
