from django.shortcuts import render, get_object_or_404
from . models import Car, OrderEntry, Service, Order
from django.views import generic

def index(request):
    cars = Car.objects.all().count()
    services = Service.objects.all().count()
    completed_services = OrderEntry.objects.filter(status__exact="complete").count()

    context = {
        'cars': cars,
        'services': services,
        'completed_services': completed_services,
    }

    return render(request, 'service/index.html', context)

def car_list(request):
    return render(request, 'service/cars.html', {
        'car_list': Car.objects.all()
        })

def car_details(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'service/car_details.html', {'cars': car})

class OrderList(generic.ListView):
    model = Order
    template_name = 'service/order_list.html'

def order_detail(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    total_price = sum(entry.price for entry in order.order_entries.all())
    return render(request, 'service/orders_detail.html', {
        'order': order, 'total_price': total_price
        })

