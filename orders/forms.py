from django import forms
from .models import Order
from profiles.models import CustomerAddress


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        
    class Media:
        js = [
            'https://code.jquery.com/jquery-3.6.0.min.js',  # Load jQuery from a CDN
            'admin/js/order_form.js',
        ]
        