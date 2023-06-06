from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from . models import Car, OrderEntry, Service, Order
from django.views import generic
from django.core.paginator import Paginator

def index(request):
    cars = Car.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    services = Service.objects.all().count()
    completed_services = OrderEntry.objects.filter(status__exact="complete").count()
    context = {
        'cars': cars,
        'services': services,
        'completed_services': completed_services,
        'num_visits': num_visits,
    }
    return render(request, 'service/index.html', context)

def car_list(request):
    qs = Car.objects
    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(licence_plate__icontains=q) |
        Q(vin_code__icontains=q) |
        Q(customer__icontains=q) |
        Q(model__model__icontains=q)
        )
    else:
        qs = qs.all()
    paginator = Paginator(qs, 2)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'service/cars.html', {
        'car_list': car_list
        })

def car_details(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'service/car_details.html', {'cars': car})

class OrderList(generic.ListView):
    model = Order
    paginate_by = 1
    template_name = 'service/order_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(date__icontains=q) |
                Q(car__customer__icontains=q) |
                Q(car__licence_plate__icontains=q) |
                Q(car__vin_code__istartswith=q) |
                Q(car__model__model__icontains=q)
            )
        return qs

def order_detail(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    # total_price = sum(entry.price for entry in order.order_entries.all())
    return render(request, 'service/orders_detail.html', {
        'order': order, 'total_price': order.price
        })


class UserOrderEntryListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'service/user_orderentry_list.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__client=self.request.user)
        return qs