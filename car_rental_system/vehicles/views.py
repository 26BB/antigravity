from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vehicle, VehicleAvailability
from .forms import VehicleForm, AvailabilityForm

@login_required
def register_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('vehicles:list')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/register.html', {'form': form})

@login_required
def vehicle_list(request):
    # Depending on role, show different lists. For now, show owner's cars.
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'vehicles/list.html', {'vehicles': vehicles})

@login_required
def manage_availability(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user)
    availabilities = vehicle.availabilities.all()

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            avail = form.save(commit=False)
            avail.vehicle = vehicle
            avail.save()
            return redirect('vehicles:manage_availability', vehicle_id=vehicle.id)
    else:
        form = AvailabilityForm()

    return render(request, 'vehicles/availability.html', {
        'vehicle': vehicle,
        'form': form,
        'availabilities': availabilities
    })
