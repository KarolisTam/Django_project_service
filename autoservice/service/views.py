from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.utils.translation import gettext_lazy as _
from . models import Car, OrderEntry, Service, Order, OrderReview
from django.views import generic
from . forms import OrderReviewForm

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
    paginate_by = 4
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

# def order_detail(request, pk: int):
#     order = get_object_or_404(Order, pk=pk)
#     # total_price = sum(entry.price for entry in order.order_entries.all())
#     return render(request, 'service/orders_detail.html', {
#         'order': order, 'total_price': order.price
#         })


class UserOrderEntryListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'service/user_orderentry_list.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__client=self.request.user)
        return qs
    

class OrderDetailReview(generic.edit.FormMixin, generic.DetailView):
    model = Order
    template_name = 'service/orders_detail.html'
    form_class = OrderReviewForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["total_price"] = sum(entry.price for entry in self.get_object().order_entries.all())
        return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['commenter'] = self.request.user
        return initial
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.order = self.get_object()
        form.instance.commenter = self.request.user
        form.save()
        messages.success(self.request, _('Review posted!'))
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})