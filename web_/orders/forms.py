from django import forms
from .models import Order, OrderItem
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'phone', 'type', 'status', 'manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()