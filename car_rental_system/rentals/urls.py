from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('search/', views.search_vehicles, name='search'),
    path('book/<int:vehicle_id>/', views.book_vehicle, name='book'),
    path('log/<int:booking_id>/', views.log_trip, name='log_trip'),
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
]
