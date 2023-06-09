from django.contrib.auth import get_user_model
from typing import Any, Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import date
from tinymce.models import HTMLField

# verbose_name   <--- nurodo ka matys klientas
# 
User = get_user_model()

class CarModel(models.Model):
    make = models.CharField(_("Make"), max_length=100, db_index=True)
    model = models.CharField(_("Model"), max_length=100, db_index=True)
    year = models.PositiveIntegerField(_("Year"), null=True, blank=True)
    engine = models.CharField(_("Engine"), max_length=100, null=True, blank=True)
    cover = models.ImageField(
        _("cover"), 
        upload_to='service/car_covers', 
        null=True,
        blank=True)

    class Meta:
        ordering = ["model", "year"]
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) {self.engine}"

    def get_absolute_url(self):
        return reverse("car model_detail", kwargs={"pk": self.pk})


class Car(models.Model):
    client = models.ForeignKey(
        User, 
        verbose_name=_("client"), 
        related_name="car",
        null=True, blank=True,
        on_delete=models.CASCADE)
    model =  models.ForeignKey(
        CarModel,
        verbose_name=('model'),
        related_name="cars",
        on_delete=models.CASCADE)
    licence_plate = models.CharField(_("Licence Plate"), max_length=20, db_index=True)
    vin_code = models.CharField(_("VIN Code"), max_length=50, db_index=True)
    note = HTMLField(_("Client note"), max_length=50, null=True, blank=True)
    foto = models.ImageField(_("foto"), upload_to='service/car_foto', null=True, blank=True)

    class Meta:
        ordering = ["licence_plate"]
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return self.licence_plate

    def get_absolute_url(self):
        return reverse("cars_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    date = models.DateField(_("data"), db_index=True, null=True, blank=True, auto_now=True)
    price = models.DecimalField(_("Price"), max_digits=18, decimal_places=2, default=0)
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        related_name="orders", 
        on_delete=models.CASCADE, 
        null=True)
    due_back = models.DateField(_("due back"), null=True, blank=True, db_index=True)

    @property
    def client(self):
        return self.car.client

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["date", "id"]
        verbose_name = _("order")
        verbose_name_plural = _("orders")


    def __str__(self):
        return f"Order Nr.{self.pk}. {self.car.client}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})


class Service(models.Model):
    name = models.CharField(_("name"), max_length=100)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)

    class Meta:
        ordering = ["name", "price"]
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    


class OrderEntry(models.Model):
    quantity = models.DecimalField(_("quantity"), max_digits=18, decimal_places=2, default=1)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    total = models.DecimalField(_("total"), max_digits=18, decimal_places=2, default=0)
    service = models.ForeignKey(
        Service,
        related_name='service',
        related_query_name="order_entries",
        on_delete=models.CASCADE)
    order= models.ForeignKey(
        Order,
        verbose_name="order",
        related_name='order_entries', 
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("order entry")
        verbose_name_plural = _("order entries")

    def __str__(self):
        return f"{self.service} {self.quantity} {self.price}"
    
    def get_absolute_url(self):
        return reverse("order entry_detail", kwargs={"pk": self.pk})
    
    def get_color(self):
        colors = {
            "new": "blue",
            "processing": "orange",
            "complete": "green",
            "cancelled": "red",
        }
        default_color = "black"
        return colors.get(self.status, default_color)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status)

    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = self.service.price
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.price = self.order.order_entries.aggregate(models.Sum("total"))["total__sum"]
        self.order.save()

    STATUS_CHOICES = [
        ("new", "New"),
        ("processing", "Processing"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(
        _("Status"),
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=0, 
        db_index=True)
    
    
class OrderReview(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"),
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    commenter = models.ForeignKey(
        User, 
        verbose_name=_("commenter"),
        related_name="order_commenter", 
        on_delete=models.CASCADE
    )
    created_at = models.DateField(_("Created"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=4000)


    class Meta:
        ordering = ['-created_at']
        verbose_name = _("order review")
        verbose_name_plural = _("order reviews")

    def __str__(self):
        return f"{self.created_at}: {self.commenter}"

    def get_absolute_url(self):
        return reverse("order review_detail", kwargs={"pk": self.pk})

