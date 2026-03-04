from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, TripLog, RentalPolicy
from vehicles.models import Vehicle, VehicleAvailability
from .forms import BookingRequestForm, TripLogForm
from datetime import datetime
from django.db.models import Q

from django.utils.dateparse import parse_datetime

@login_required
def search_vehicles(request):
    vehicles = Vehicle.objects.filter(status='active')

    start_str = request.GET.get('start')
    end_str = request.GET.get('end')

    searched = False

    if start_str and end_str:
        searched = True
        start_dt = parse_datetime(start_str)
        end_dt = parse_datetime(end_str)

        if start_dt and end_dt and start_dt < end_dt:
            req_day = start_dt.weekday()
            req_start_time = start_dt.time()
            req_end_time = end_dt.time()

            available_vehicles = []
            for v in vehicles:
                has_slot = VehicleAvailability.objects.filter(
                    vehicle=v,
                    day_of_week=req_day,
                    start_time__lte=req_start_time,
                    end_time__gte=req_end_time
                ).exists()

                if has_slot:
                    overlapping = Booking.objects.filter(
                        vehicle=v,
                        status__in=['approved', 'requested', 'active'],
                        start_time__lt=end_dt,
                        end_time__gt=start_dt
                    ).exists()

                    if not overlapping:
                        available_vehicles.append(v)
            vehicles = available_vehicles
        else:
            vehicles = []

    return render(request, 'rentals/search.html', {'vehicles': vehicles, 'searched': searched})

@login_required
def book_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, status='active')
    policy = RentalPolicy.objects.filter(is_active=True).first() # Grab the latest active policy

    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.driver = request.user
            booking.vehicle = vehicle
            booking.policy = policy
            booking.save()
            return redirect('rentals:search') # Redirect to dashboard in future
    else:
        form = BookingRequestForm()

    return render(request, 'rentals/book.html', {
        'vehicle': vehicle,
        'form': form,
        'policy': policy
    })

@login_required
def log_trip(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, driver=request.user)

    if request.method == 'POST':
        form = TripLogForm(request.POST)
        if form.is_valid():
            trip_log = form.save(commit=False)
            trip_log.booking = booking
            trip_log.save()
            booking.status = 'completed'
            booking.save()
            return redirect('rentals:search')
    else:
        form = TripLogForm()

    return render(request, 'rentals/log_trip.html', {'form': form, 'booking': booking})

from django.utils import timezone

@login_required
def approve_booking(request, booking_id):
    if request.method == 'POST':
        # Ensure the logged-in user actually owns the vehicle being booked
        booking = get_object_or_404(Booking, id=booking_id, vehicle__owner=request.user, status='requested')

        action = request.POST.get('action')
        if action == 'approve':
            booking.status = 'approved'
            booking.approved_at = timezone.now()
        elif action == 'deny':
            booking.status = 'cancelled'

        booking.save()

    return redirect('dashboard')
