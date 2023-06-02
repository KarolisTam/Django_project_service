from typing import Any, Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# verbose_name   <--- nurodo ka matys klientas
# 

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
    licence_plate = models.CharField(_("Licence Plate"), max_length=20, db_index=True)
    vin_code = models.CharField(_("VIN Code"), max_length=50, db_index=True)
    customer = models.CharField(_("client"), max_length=50)
    model =  models.ForeignKey(
        CarModel,
        verbose_name=('model'),
        related_name="cars",
        on_delete=models.CASCADE)

    class Meta:
        ordering = ["licence_plate"]
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return self.licence_plate

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    date = models.DateField(_("data"), db_index=True)
    price = models.DecimalField(_("Price"), max_digits=18, decimal_places=2, default=0)
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        related_name="orders", 
        on_delete=models.CASCADE, 
        null=True)

    class Meta:
        ordering = ["date", "id"]
        verbose_name = _("order")
        verbose_name_plural = _("orders")


    def __str__(self):
        return f"Order #{self.pk}"

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