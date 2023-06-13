from django import forms
from . import models
from .models import Order, Car

class DateInput(forms.DateInput):
    input_type = 'date'


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = models.OrderReview
        fields = ('content', 'order', 'commenter')
        widgets = {
            'order': forms.HiddenInput(),
            'commenter': forms.HiddenInput(),}


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ("due_back", "car")
        widgets = {'due_back': DateInput()}


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ('model', 'licence_plate', 'vin_code', 'client', 'foto')
        widgets = {'due_back': DateInput(),
                   'client': forms.HiddenInput()}


