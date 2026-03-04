from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('register/', views.register_vehicle, name='register'),
    path('availability/<int:vehicle_id>/', views.manage_availability, name='manage_availability'),
    path('list/', views.vehicle_list, name='list'),
]
