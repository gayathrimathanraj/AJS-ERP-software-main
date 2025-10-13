from django import forms
from .models import Material, Taxes, Warehouse, Customer

class TaxesForm(forms.ModelForm):
    class Meta:
        model = Taxes
        fields = ['hsn_code']  # ONLY HSN Code in form
        widgets = {
            'hsn_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'HSN Code...',
            }),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            'material_name', 'uom', 'category', 'model', 'brand',
            'description', 'image', 'active_status', 'taxes'
        ]

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = [
            'warehouse_code', 'warehouse_name', 'contact_number', 'email_address',
            'state_of_supply', 'gst_number', 'address1', 'description',
            'city', 'state', 'country', 'postal_code'
        ]
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_name', 'contact_person', 'contact_number',
            'email_address', 'alt_contact_no', 'customer_group', 'category',
            'gst_number', 'pan_no', 'credit_period', 'credit_limit', 'state_of_supply',
            'image', 'same_as_billing',
            'billing_address1', 'billing_address2', 'billing_city', 'billing_state', 
            'billing_country', 'billing_postal_code',
            'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state',
            'shipping_country', 'shipping_postal_code'
        ]