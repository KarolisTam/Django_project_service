from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("cars/", views.car_list , name="car_list"),
    path("cars/<int:pk>/", views.car_details, name="cars_detail"),
    path("orders/", views.OrderList.as_view(), name='order_list'),
    path("orders/<int:pk>/", views.order_detail, name='order_detail')
]