from django import forms
from . import models

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = models.OrderReview
        fields = ('content', 'order', 'commenter')
        widgets = {
            'order': forms.HiddenInput(),
            'commenter': forms.HiddenInput(),
        }