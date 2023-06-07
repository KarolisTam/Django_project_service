from django.contrib import admin
from . import models
from .models import OrderEntry
# Register your models here.

class OrderEntryInLine(admin.TabularInline):      # Pasiema oderentery lentele
    model = OrderEntry
    extra = 0


class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'service')
    list_filter = ('order', 'status')
    list_editable = ('status', )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'car', "due_back", 'date')
    inlines = [OrderEntryInLine]    # Prideda OderEntry lente po oder, kad galima butu prideti dar viena 


class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'licence_plate', 'model', 'note')
    list_filter = ('model', 'note')
    search_fields = ('licence_plate', 'vin_code')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'commenter', 'order', 'content')

admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry, OrderEntryAdmin)
admin.site.register(models.OrderReview, OrderReviewAdmin)