from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking
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
