from django.contrib import admin
from .models import Vehicle, VehicleAvailability

class VehicleAvailabilityInline(admin.TabularInline):
    model = VehicleAvailability
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'license_plate', 'owner', 'status')
    list_filter = ('status', 'make', 'year')
    search_fields = ('license_plate', 'owner__username', 'make', 'model')
    inlines = [VehicleAvailabilityInline]

admin.site.register(VehicleAvailability)
