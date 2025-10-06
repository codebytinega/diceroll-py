from django import forms
from .models import Sale
from inventory.models import Product


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold', 'customer_name', 'notes']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'quantity_sold': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'min': '1',
                'placeholder': '1'
            }),
            'customer_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter customer name (optional)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Additional notes about this sale (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show products that are in stock
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0).order_by('name')
        self.fields['product'].empty_label = "Select a product"
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity_sold = cleaned_data.get('quantity_sold')
        
        if product and quantity_sold:
            if not product.can_sell(quantity_sold):
                raise forms.ValidationError(
                    f"Insufficient stock for {product.name}. "
                    f"Available: {product.quantity}, Requested: {quantity_sold}"
                )
        
        return cleaned_data