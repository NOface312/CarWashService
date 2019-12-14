from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User

from .models import Order

class OrderCreatingForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('order_date',)
