from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle
from rentals.models import Booking, TripLog
from accounts.models import User
from django.db.models import Sum

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role == 'Admin':
            return render_admin_dashboard(request)
        elif request.user.role == 'owner':
            return render_owner_dashboard(request)
        elif request.user.role == 'driver':
            return render_driver_dashboard(request)
        else:
            return render(request, 'dashboard/welcome.html')
    else:
        return render(request, 'dashboard/welcome.html')

def render_owner_dashboard(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    # Get bookings for vehicles owned by this user
    pending_bookings = Booking.objects.filter(vehicle__owner=request.user, status='requested')
    active_bookings = Booking.objects.filter(vehicle__owner=request.user, status='active')
    
    return render(request, 'dashboard/owner.html', {
        'vehicles': vehicles,
        'pending_bookings': pending_bookings,
        'active_bookings': active_bookings
    })

def render_driver_dashboard(request):
    my_bookings = Booking.objects.filter(driver=request.user).order_by('-start_time')
    return render(request, 'dashboard/driver.html', {
        'bookings': my_bookings
    })

@login_required
def render_admin_dashboard(request):
    # System Health Metrics
    total_vehicles = Vehicle.objects.count()
    total_users = User.objects.count()
    active_rentals = Booking.objects.filter(status='active').count()
    
    # Calculate Total Revenue
    completed_trips = TripLog.objects.all()
    total_revenue = sum(trip.total_cost for trip in completed_trips)
    
    # Recent Activity Feed
    recent_bookings = Booking.objects.all().order_by('-requested_at')[:5]
    recent_completed = TripLog.objects.all().order_by('-logged_at')[:5]
    
    return render(request, 'dashboard/admin.html', {
        'total_vehicles': total_vehicles,
        'total_users': total_users,
        'active_rentals': active_rentals,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'recent_completed': recent_completed
    })
