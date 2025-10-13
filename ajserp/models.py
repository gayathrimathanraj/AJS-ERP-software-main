from django.db import models

# Create your models here.
class Taxes(models.Model):
    hsn_code = models.CharField(max_length=20, primary_key=True)
    cgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    igst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cess = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.hsn_code


# class Material(models.Model):
#     material_code = models.CharField(max_length=50,  primary_key=True) 
#     material_name = models.CharField(max_length=255)
#     uom = models.CharField(max_length=50)
#     category = models.CharField(max_length=100)
#     model = models.CharField(max_length=100, blank=True, null=True)
#     brand = models.CharField(max_length=100, blank=True, null=True)
#     description = models.TextField(max_length=30, blank=True, null=True)
#     image = models.ImageField(upload_to='materials/', blank=True, null=True)
#     active_status = models.BooleanField(default=True)
#     taxes=models.ForeignKey(
#         Taxes,on_delete=models.CASCADE,
#         to_field='hsn_code',   # <-- explicitly link to hsn_code (CharField PK)
#         db_column='hsn_code'
#     )

#     def __str__(self):
#         return self.material_name

class Material(models.Model):
    material_code = models.CharField(max_length=50, primary_key=True, editable=False)
    material_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    model = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    active_status = models.BooleanField(default=True)
    taxes = models.ForeignKey(
        Taxes, on_delete=models.CASCADE,
        to_field='hsn_code',
        db_column='hsn_code'
    )

    def save(self, *args, **kwargs):
        if not self.material_code:
            # Generate code like: MAT0001, MAT0002, etc.
            last_material = Material.objects.order_by('material_code').last()
            if last_material:
                last_number = int(last_material.material_code[3:])  # Extract number from "MAT0001"
                new_number = last_number + 1
            else:
                new_number = 1
            self.material_code = f"MAT{new_number:04d}"  # MAT0001, MAT0002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return self.material_name

class Warehouse(models.Model):
    warehouse_code = models.CharField(max_length=10, primary_key=True)
    warehouse_name = models.CharField(max_length=70)
    contact_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    state_of_supply = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=15)
    address1 = models.TextField()
    description = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=6)

    def __str__(self):
        return self.warehouse_name
    
class Customer(models.Model):
    # customer_code = models.CharField(max_length=50, primary_key=True)
    customer_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    alt_contact_no = models.CharField(max_length=15, blank=True, null=True)
    customer_group = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    gst_number = models.CharField(max_length=15)
    pan_no = models.CharField(max_length=10)
    credit_period = models.IntegerField(default=0)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    state_of_supply = models.CharField(max_length=100)
    image = models.ImageField(upload_to='customers/', blank=True, null=True)
    billing_address1 = models.TextField()
    billing_address2 = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100, default='India')
    billing_postal_code = models.CharField(max_length=10)
    shipping_address1 = models.TextField()
    shipping_address2 = models.TextField(blank=True, null=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100, default='India')
    shipping_postal_code = models.CharField(max_length=10)
    same_as_billing = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name 