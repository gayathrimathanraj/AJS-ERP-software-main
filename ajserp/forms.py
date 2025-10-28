from django import forms
from .models import Material, Taxes, Warehouse, Customer, CustomerGroup, CustomerCategory, Supplier, SupplierGroup, SupplierCategory, MaterialInward  
from datetime import date

class TaxesForm(forms.ModelForm):
    class Meta:
        model = Taxes
        fields = ['hsn_code', 'cgst', 'sgst', 'igst', 'cess']  # ALL tax fields
        widgets = {
            'hsn_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'HSN Code...',
                'required': True,
            }),
            'cgst': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'CGST %',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'required': True
            }),
            'sgst': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'SGST %',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'required': True
            }),
            'igst': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'IGST %',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'required': True
            }),
            'cess': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'CESS %',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'required': True
            }),
        }

# class MaterialForm(forms.ModelForm):
#     class Meta:
#         model = Material
#         fields = [
#             'material_name', 'uom', 'category', 'model', 'brand',
#             'description', 'image', 'active_status', 'taxes'
#         ]

# class MaterialForm(forms.ModelForm):
#     class Meta:
#         model = Material
#         fields = [
#             'category', 'material_name', 'uom', 'model', 'brand',
#             'description', 'image', 'active_status', 'taxes'
#         ]
#         widgets = {
#             'material_code': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Auto-generated'
#             }),
#             'category': forms.Select(attrs={
#                 'class': 'form-select',
#                 'id': 'category'
#             }),
#             'model': forms.Select(attrs={
#                 'class': 'form-select',
#             }),
#             'brand': forms.Select(attrs={
#                 'class': 'form-select',
#             })
            
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Remove the category queryset override since we're using choices
        

# class WarehouseForm(forms.ModelForm):
#     class Meta:
#         model = Warehouse
#         fields = [
#             'warehouse_code', 'warehouse_name', 'contact_number', 'email_address',
#             'state_of_supply', 'gst_number', 'address1', 'description',
#             'city', 'state', 'country', 'postal_code'
#         ]
        
# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         exclude = ['customer_code']  # Exclude auto-generated field
#         fields = [
#             'customer_name', 'contact_person', 'contact_number',
#             'email_address', 'alt_contact_no', 'customer_group', 'category',
#             'gst_number', 'pan_no', 'credit_period', 'credit_limit', 'state_of_supply',
#             'image', 'same_as_billing',
#             'billing_address1', 'billing_address2', 'billing_city', 'billing_state', 
#             'billing_country', 'billing_postal_code',
#             'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state',
#             'shipping_country', 'shipping_postal_code'
#         ]
#         widgets = {
#             'customer_group': forms.Select(attrs={
#                 'class': 'form-select',
#             }),
#             'category': forms.Select(attrs={
#                 'class': 'form-select',
#             })
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Set querysets for the foreign key fields
#         self.fields['customer_group'].queryset = CustomerGroup.objects.all()
#         self.fields['category'].queryset = CustomerCategory.objects.all()
        
#         # Set empty labels
#         self.fields['customer_group'].empty_label = "Select Customer Group"
#         self.fields['category'].empty_label = "Select Customer Category"
        
#         self.fields['category'].empty_label = "Select Customer Category"

# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         exclude = ['vendor_code']  # Exclude auto-generated field
#         fields = [
#             'vendor_name', 'contact_person', 'contact_number',
#             'email_address', 'alt_contact_no', 'supplier_group', 'category',
#             'gst_number', 'pan_no', 'credit_period', 'credit_limit', 'state_of_supply',
#             'image', 'same_as_billing',
#             'billing_address1', 'billing_address2', 'billing_city', 'billing_state', 
#             'billing_country', 'billing_postal_code',
#             'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state',
#             'shipping_country', 'shipping_postal_code'
#         ]
#         widgets = {
#             'supplier_group': forms.Select(attrs={
#                 'class': 'form-select',
#             }),
#             'category': forms.Select(attrs={
#                 'class': 'form-select',
#             })
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Set querysets for the foreign key fields
#         self.fields['supplier_group'].queryset = SupplierGroup.objects.all()
#         self.fields['category'].queryset = SupplierCategory.objects.all()
        
#         # Set empty labels
#         self.fields['supplier_group'].empty_label = "Select Supplier Group"
#         self.fields['category'].empty_label = "Select Supplier Category"
        
# class MaterialInwardForm(forms.ModelForm):
#     class Meta:
#         model = MaterialInward
#         fields = [
#             'category', 'grn_number', 'grn_date', 'batch', 'vendor',
#             'invoice_number', 'invoice_date', 'quantity', 'material_name', 
#             'uom', 'model', 'brand', 'taxes', 'vendor_name'
#         ]
#         widgets = {
#             # Selection fields (Dropdowns)
#             'category': forms.Select(attrs={
#                 'class': 'form-select',
#                 'id': 'category'
#             }),
#             'vendor': forms.Select(attrs={
#                 'class': 'form-select',
#                 'id': 'vendor_select'
#             }),
#             'model': forms.Select(attrs={
#                 'class': 'form-select',
#             }),
#             'brand': forms.Select(attrs={
#                 'class': 'form-select',
#             }),
#             'taxes': forms.Select(attrs={
#                 'class': 'form-select',
#             }),
            
#             # Manual input fields
#             'grn_number': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter GRN number'
#             }),
#             'grn_date': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date'
#             }),
#             'batch': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter batch number'
#             }),
#             'invoice_number': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter invoice number'
#             }),
#             'invoice_date': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date'
#             }),
#             'quantity': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter quantity',
#                 'step': '0.01',
#                 'min': '0'
#             }),
#             'material_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter material name'
#             }),
#             'uom': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter unit of measurement'
#             }),
#             'vendor_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter vendor name'
#             })
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Remove the auto-generated field from form since you want it manual
#         # If you want material_code to be manual too, add it to fields and widgets
        
# class PriceSearchForm(forms.Form):
#     material_code = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Material Code'
#         })
#     )
    
#     material_name = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Material Name'
#         })
#     )
    
#     category = forms.ChoiceField(
#         required=False,
#         choices=[
#             ('', 'All Categories'),
#             ('Service', 'Service'),
#             ('Spare', 'Spare'),
#             ('Material', 'Material'),
#         ],
#         widget=forms.Select(attrs={
#             'class': 'form-control'
#         })
#     )
    
#     model = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Model'
#         })
#     )
    
#     status = forms.ChoiceField(
#         required=False,
#         choices=[
#             ('', 'All Status'),
#             ('Active', 'Active'),
#             ('Inactive', 'Inactive'),
#         ],
#         widget=forms.RadioSelect()
#     )
    
#     # Add MRP range fields
#     min_mrp = forms.DecimalField(
#         required=False,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.01',
#             'min': '0',
#             'placeholder': 'Min MRP'
#         })
#     )
    
#     max_mrp = forms.DecimalField(
#         required=False,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.01',
#             'min': '0',
#             'placeholder': 'Max MRP'
#         })
#     )
    
#     # Add Selling Price range fields
#     min_selling_price = forms.DecimalField(
#         required=False,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.01',
#             'min': '0',
#             'placeholder': 'Min Selling Price'
#         })
#     )
    
#     max_selling_price = forms.DecimalField(
#         required=False,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.01',
#             'min': '0',
#             'placeholder': 'Max Selling Price'
#         })
#     )
    
#     # ADD EXACT PRICE SEARCH FIELDS HERE
#     exact_mrp = forms.DecimalField(
#         required=False,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.01',
#             'min': '0',
#             'placeholder': 'Exact MRP'
#         })
#     )
    
#     exact_selling_price = forms.DecimalField(
#         required=False,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.01',
#             'min': '0',
#             'placeholder': 'Exact Selling Price'
#         })
#     )
    
#     # Price type filter (optional)
#     price_type = forms.ChoiceField(
#         required=False,
#         choices=[
#             ('', 'All Prices'),
#             ('mrp', 'MRP Only'),
#             ('selling', 'Selling Price Only'),
#             ('both', 'Both Prices'),
#         ],
#         widget=forms.Select(attrs={
#             'class': 'form-control'
#         })
#     )
    
    
#     from_date = forms.DateField(
#         required=False,
#         widget=forms.DateInput(attrs={
#             'class': 'form-control',
#             'type': 'date'
#         })
#     )
    
#     to_date = forms.DateField(
#         required=False,
#         widget=forms.DateInput(attrs={
#             'class': 'form-control',
#             'type': 'date'
#         })
#     )
    
#     def clean(self):
#         cleaned_data = super().clean()
#         from_date = cleaned_data.get('from_date')
#         to_date = cleaned_data.get('to_date')
#         min_mrp = cleaned_data.get('min_mrp')
#         max_mrp = cleaned_data.get('max_mrp')
#         min_selling_price = cleaned_data.get('min_selling_price')
#         max_selling_price = cleaned_data.get('max_selling_price')
#         exact_mrp = cleaned_data.get('exact_mrp')
#         exact_selling_price = cleaned_data.get('exact_selling_price')
        
#         # Validate date range
#         if from_date and to_date:
#             if from_date > to_date:
#                 raise forms.ValidationError("From date cannot be greater than To date")
        
#         # Validate MRP range
#         if min_mrp and max_mrp:
#             if min_mrp > max_mrp:
#                 raise forms.ValidationError("Min MRP cannot be greater than Max MRP")
        
#         # Validate Selling Price range
#         if min_selling_price and max_selling_price:
#             if min_selling_price > max_selling_price:
#                 raise forms.ValidationError("Min Selling Price cannot be greater than Max Selling Price")
        
#         # Validate that selling price is not greater than MRP in ranges
#         if min_mrp and min_selling_price and min_selling_price > min_mrp:
#             raise forms.ValidationError("Selling price cannot be greater than MRP")
        
#         if max_mrp and max_selling_price and max_selling_price > max_mrp:
#             raise forms.ValidationError("Selling price cannot be greater than MRP")
        
#           # Validate exact prices
#         if exact_mrp and exact_selling_price and exact_selling_price > exact_mrp:
#             raise forms.ValidationError("Selling price cannot be greater than MRP")
        
#         # Validate that user doesn't use both range and exact search for same field
#         if exact_mrp and (min_mrp or max_mrp):
#             raise forms.ValidationError("Please use either exact MRP or MRP range, not both")
        
#         if exact_selling_price and (min_selling_price or max_selling_price):
#             raise forms.ValidationError("Please use either exact Selling Price or Selling Price range, not both")
        
#         return cleaned_data
    
    