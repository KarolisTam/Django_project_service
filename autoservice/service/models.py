from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# verbose_name   <--- nurodo ka matys klientas
# 

class CarModel(models.Model):
    make = models.CharField(_("Make"), max_length=100)
    model = models.CharField(_("Model"), max_length=100)
    year = models.PositiveIntegerField(_("Year"))
    engine = models.CharField(_("Engine"), max_length=100)

    class Meta:
        ordering = ["make", "model", "year", "engine"]
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) {self.engine}"

    def get_absolute_url(self):
        return reverse("car model_detail", kwargs={"pk": self.pk})


class Car(models.Model):
    licence_plate = models.CharField(_("Licence Plate"), max_length=20, db_index=True)
    vin_code = models.CharField(_("VIN Code"), max_length=50, db_index=True)
    customer = models.CharField(_("client"), max_length=50, db_index=True)
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
    date = models.CharField(_("data"), max_length=50, db_index=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, db_index=True)
    car = models.ForeignKey(
        Car, 
        verbose_name=('car'), 
        related_name="orders",
        on_delete=models.CASCADE)

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
    price = models.IntegerField(_("price"))

    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return self.name


class OrderList(models.Model):
    quantity = models.CharField(_("quantity"), max_length=50)
    price = models.CharField(_("price"), max_length=50)
    service = models.ForeignKey(
        Service,
        related_name='service',
        on_delete=models.CASCADE)
    order= models.ForeignKey(
        Order,
        related_name='order', 
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("order List")
        verbose_name_plural = _("order Lists")

    def __str__(self):
        return f"OrderList #{self.pk}"