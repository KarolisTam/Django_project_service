from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("cars/", views.car_list , name="car_list"),
    path("cars/<int:pk>/", views.car_details, name="cars_detail"),
    path("orders/", views.OrderList.as_view(), name='order_list'),
    path("orders/<int:pk>/", views.OrderDetailReview.as_view(), name='order_detail'),
    path("my/cars/", views.UserCarListView.as_view(), name="user_cars"),
    path("my/car/create/", views.CarCreateView.as_view(), name="user_car_create"),
    path("my/car/<int:pk>/update/", views.CarUpdateView.as_view(), name="user_car_update"),
    path("my/orders/", views.UserOrderListView.as_view(), name="user_orders"),
    path("my/order/create/", views.OrderCreateView.as_view(), name="user_order_create"),
    path("my/order/<int:pk>/delete/", views.OrderDeleteView.as_view(), name='delete_order'),
]