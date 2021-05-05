from django_filters import FilterSet, CharFilter, DateFilter

from .models import Flight


class FlightFilter(FilterSet):
    boarding = CharFilter(lookup_expr='icontains')
    destination = CharFilter(lookup_expr='icontains')
    flight_date = DateFilter(lookup_expr='exact')

    class Meta:
        model = Flight
        fields = ['boarding', 'destination', 'flight_date']
