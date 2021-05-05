from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('flights', views.FlightList.as_view(), name='flight_list'),
    path('flights/create', views.FlightCreateView.as_view(), name='flight_create'),
    path('flights/<int:pk>/update',
         views.FlightUpdateView.as_view(), name='flight_update'),
    path('flights/<int:pk>/book-flight',
         views.FlightBookingView.as_view(), name='admin_flight_reserve'),
    path('reserve-flight/<int:pk>', views.bookFlight, name='reserve_flight'),
    path('cancel-flight/<int:pk>', views.cancelFlight, name='cancel_flight'),
    path('delete-flight/<int:pk>', views.deleteFlight, name='delete_flight'),
]
