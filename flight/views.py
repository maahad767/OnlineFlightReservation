from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django_filters.views import FilterView

from .models import Flight
from .filters import FlightFilter


class HomePageView(View):
    template_name = 'flight/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class FlightList(FilterView):
    filterset_class = FlightFilter
    template_name = 'flight/flight_list.html'
    paginate_by = 100
    ordering = ['flight_date', 'flight_time']

    def get_queryset(self, **kwargs):
        return Flight.objects.filter(status='available')


class FlightCreateView(CreateView):
    model = Flight
    fields = '__all__'
    success_url = reverse_lazy('admin-dashboard')


class FlightUpdateView(UpdateView):
    model = Flight
    fields = '__all__'
    success_url = reverse_lazy('admin-dashboard')


class FlightBookingView(UpdateView):
    model = Flight
    fields = ['destination', 'boarding',
              'flight_date', 'flight_time', 'booked_by']
    success_url = reverse_lazy('admin-dashboard')
    template_name = 'flight/flight_book.html'

    def form_valid(self, form):
        flight = form.save(commit=False)
        flight.status = 'booked'
        flight.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


@login_required(login_url='login')
def bookFlight(request, pk):
    user = request.user

    if user.is_superuser:
        print("You can not book flight for yourself, you're a * admin!")

    flight = get_object_or_404(Flight, id=pk)
    flight.booked_by = user
    flight.status = 'booked'
    flight.save()

    if request.user.is_superuser:
        return redirect('admin-dashboard')

    return redirect('user-dashboard')


@login_required(login_url='login')
def cancelFlight(request, pk, user=None):
    flight = get_object_or_404(Flight, id=pk)
    flight.status = 'cancelled'
    flight.save()

    flight.id = None
    flight.status = 'available'
    flight.booked_by = None
    flight.save()

    if request.user.is_superuser:
        return redirect('admin-dashboard')

    return redirect('user-dashboard')


@login_required(login_url='login')
def deleteFlight(request, pk):
    if not request.user.is_superuser:
        return redirect('user-dashboard')

    flight = get_object_or_404(Flight, id=pk)
    flight.delete()

    return redirect('admin-dashboard')
