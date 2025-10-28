from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class HSNCode(models.Model):
    """Simple HSN Code with only primary key - no tax rates, no foreign keys"""
    hsn_code = models.CharField(max_length=10, primary_key=True, verbose_name="HSN Code")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "HSN Code"
        verbose_name_plural = "HSN Codes"
        ordering = ['hsn_code']
    
    def __str__(self):
        return self.hsn_code

class Taxes(models.Model):
    # HSN Code as ForeignKey - Django automatically validates existence
    hsn_code = models.ForeignKey(
        HSNCode,
        on_delete=models.CASCADE,
        to_field='hsn_code',  # References HSNCode primary key
        db_column='hsn_code',
        verbose_name="HSN Code"
    )
    cgst = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sgst = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    igst = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cess = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tax Rate"
        verbose_name_plural = "Tax Rates"
    
    def __str__(self):
        return f"{self.hsn_code.hsn_code} - CGST:{self.cgst}% SGST:{self.sgst}%"
    

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
    

    
    # models.py - All tables as primary keys

# 1. Supplier Group - Primary Key
class SupplierGroup(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

# 2. Supplier Category - Primary Key  
class SupplierCategory(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

# 3. Customer Group - Primary Key
class CustomerGroup(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

# 4. Customer Category - Primary Key
class CustomerCategory(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
class Customer(models.Model):
    customer_code = models.CharField(max_length=50, unique=True, editable=False)
    customer_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    alt_contact_no = models.CharField(max_length=15, blank=True, null=True)
     # Change these to ForeignKey
    customer_group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='code',
        db_column='customer_group_code'
    )
    category = models.ForeignKey(
        CustomerCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='code',
        db_column='customer_category_code'
    )
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
    
class Supplier(models.Model):
    vendor_code = models.CharField(max_length=50, unique=True, editable=False)
    vendor_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    alt_contact_no = models.CharField(max_length=15, blank=True, null=True)
    
    # ForeignKey to SupplierGroup and SupplierCategory (which you already have)
    supplier_group = models.ForeignKey(
        SupplierGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='code',
        db_column='supplier_group_code'
    )
    category = models.ForeignKey(
        SupplierCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='code',
        db_column='supplier_category_code'
    )
    
    gst_number = models.CharField(max_length=15)
    pan_no = models.CharField(max_length=10)
    credit_period = models.IntegerField(default=0)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    state_of_supply = models.CharField(max_length=100)
    image = models.ImageField(upload_to='suppliers/', blank=True, null=True)
    
    # Billing Address
    billing_address1 = models.TextField()
    billing_address2 = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100, default='India')
    billing_postal_code = models.CharField(max_length=10)
    
    # Shipping Address
    shipping_address1 = models.TextField()
    shipping_address2 = models.TextField(blank=True, null=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100, default='India')
    shipping_postal_code = models.CharField(max_length=10)
    same_as_billing = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            # Generate code like: VEN001, VEN002, etc.
            last_supplier = Supplier.objects.order_by('vendor_code').last()
            if last_supplier:
                try:
                    last_number = int(last_supplier.vendor_code[3:])  # Extract number from "VEN001"
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.vendor_code = f"VEN{new_number:03d}"  # VEN001, VEN002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return self.vendor_name   
    
# 6. Material Model - Primary Key
class MaterialModel(models.Model):
     name = models.CharField(max_length=50,  primary_key=True)
     description = models.TextField(blank=True, null=True)
   
     def __str__(self):
        return self.name
    
# 7. Material Brand - Primary Key
class MaterialBrand(models.Model):
      name = models.CharField(max_length=50,  primary_key=True)
      description = models.TextField(blank=True, null=True)
   
      def __str__(self):
         return self.name



class Material(models.Model):
     # UNIQUE + NOT NULL ForeignKey to Taxes
    # taxes = models.ForeignKey(
    #     Taxes, 
    #     on_delete=models.CASCADE,
    #     to_field='hsn_code',
    #     db_column='hsn_code',
    #     verbose_name="HSN Code",
    #     null=False,           # NOT NULL constraint
    #     blank=False,          # Not allowed to be blank in forms
    #     unique=True          # UNIQUE constraint
    # )
    
    
    # CATEGORY is the PRIMARY KEY (from dropdown selection)
    category = models.CharField(
        max_length=20, 
        primary_key=True,
        choices=[
            ('Service', 'Service'),
            ('Spare', 'Spare'),
            ('Material', 'Material'),
        ]
    )
    
    # Material code is auto-generated based on category selection
    material_code = models.CharField(max_length=50, editable=False)
    
    material_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=50)
    hsn_code = models.CharField(max_length=10)
    
     # ADD THIS FOREIGN KEY FOR CURRENT PRICE
    current_price = models.ForeignKey(
        'PriceList',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_for_material',
        verbose_name="Current Price"
    )
    # Foreign keys for model and branb
    model = models.ForeignKey(
        MaterialModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='name',
        db_column='model_name'
    )
    
    brand = models.ForeignKey(
        MaterialBrand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='name',
        db_column='brand_name'
    )
      # Add these two new fields
    # mrp = models.DecimalField(
    #     max_digits=15, 
    #     decimal_places=2, 
    #     default=0.00,
    #     null=True,      # Allow null
    #     blank=True,     # Allow blank in forms
    #     verbose_name="MRP"
    # )
    # selling_price = models.DecimalField(
    #     max_digits=15, 
    #     decimal_places=2, 
    #     default=0.00,
    #     null=True,      # Allow null
    #     blank=True,     # Allow blank in forms
    #     verbose_name="Selling Price"
    # )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    active_status = models.BooleanField(default=True)
    # taxes = models.ForeignKey(
    #     Taxes, 
    #     on_delete=models.CASCADE,
    #     to_field='hsn_code',
    #     db_column='hsn_code'
    # )

    def save(self, *args, **kwargs):
        if not self.material_code:
            # Define prefixes for material codes based on category
            category_prefixes = {
                'Service': 'SESL',
                'Spare': 'SPSL', 
                'Material': 'FGSL'
            }
            
            prefix = category_prefixes.get(self.category, 'MAT')
            
            # Get last material in this category
            last_material = Material.objects.filter(
                category=self.category
            ).order_by('material_code').last()
            
            if last_material:
                try:
                    # Extract number from material code (e.g., "SESL00001" -> 1)
                    last_number = int(last_material.material_code[4:])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
                
            self.material_code = f"{prefix}{new_number:05d}"  # SESL00001, SPSL00001, FGSL00001
        
        super().save(*args, **kwargs)
    # def get_current_price(self):
    #     """Get current active price from PriceList"""
    #     try:
    #         current_price = self.prices.filter(
    #             is_active=True,
    #             from_date__lte=timezone.now().date()
    #         ).latest('from_date')
    #         return current_price
    #     except PriceList.DoesNotExist:
    #         return None

    # def get_mrp(self):
    #     """Get current MRP price"""
    #     current_price = self.get_current_price()
    #     return current_price.mrp_price if current_price else 0

    # def get_selling_price(self):
    #     """Get current selling price"""
    #     current_price = self.get_current_price()
    #     return current_price.selling_price if current_price else 0
    def get_current_price_display(self):
        """Get current price for display - uses the foreign key"""
        if self.current_price:
            return self.current_price
        # Fallback to latest active price if no current_price set
        try:
            return self.prices.filter(is_active=True).latest('from_date')
        except PriceList.DoesNotExist:
            return None

    def __str__(self):
         return f"{self.material_code} - {self.material_name}"
     

    
class PriceList(models.Model):
    PRICING_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        
    ]
    
    material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='prices',
        to_field='category',
        db_column='material_category'
    )
    mrp_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    pricing_status = models.CharField(
        max_length=10, 
        choices=PRICING_STATUS_CHOICES, 
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['material', 'from_date']
        ordering = ['-from_date'] 
    
    def save(self, *args, **kwargs):
        # Auto-update pricing_status based on dates
        today = timezone.now().date()
        
        if self.from_date > today:
            self.pricing_status = 'Upcoming'
        elif self.to_date and self.to_date < today:
            self.pricing_status = 'Expired'
            self.is_active = False
        elif self.is_active:
            self.pricing_status = 'Active'
        else:
            self.pricing_status = 'Inactive'
            
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.material.material_code} - MRP: {self.mrp_price}, Selling: {self.selling_price} ({self.pricing_status})"
    
class MaterialInward(models.Model):
    CATEGORY_CHOICES = [
        ('Service', 'Service'),
        ('Spare', 'Spare'), 
        ('Material', 'Material'),
    ]
    
    # Auto-generated primary key
    id = models.AutoField(primary_key=True)
    
    
    
    # Auto-generated fields
    grn_number = models.CharField(max_length=50, unique=True, editable=False)
    batch = models.CharField(max_length=100, unique=True, editable=False)
    
    # Dates
    grn_date = models.DateField(default=timezone.now)
    invoice_date = models.DateField()
    
    # Manual entry fields
    invoice_number = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Category - will be auto-filled from material master (NOT primary key)
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True
    )
    
    # Material details - will be auto-filled when material is selected
    material_code = models.CharField(max_length=50, editable=False)
    material_name = models.CharField(max_length=255, editable=False)
    uom = models.CharField(max_length=50, editable=False)
    
    vendor = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        to_field='vendor_code',
        db_column='vendor_code',
        verbose_name="Vendor"
    )
    
    vendor_name = models.CharField(max_length=255, editable=False)
    
    model = models.ForeignKey(
        MaterialModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='name',
        db_column='model_name'
    )
    
    brand = models.ForeignKey(
        MaterialBrand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='name',
        db_column='brand_name'
    )
    
    hsn_code = models.ForeignKey(
        HSNCode,
        on_delete=models.CASCADE,
        to_field='hsn_code',
        db_column='hsn_code',
        verbose_name="HSN Code"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Material Inward"
        verbose_name_plural = "Material Inwards"
        ordering = ['-grn_date', '-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate GRN Number
        if not self.grn_number:
            last_grn = MaterialInward.objects.order_by('-id').first()
            if last_grn and last_grn.grn_number:
                try:
                    last_number = int(last_grn.grn_number[3:])  # Extract number from GRN001
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.grn_number = f"GRN{new_number:05d}"  # GRN00001, GRN00002

        # Auto-generate Batch Number
        if not self.batch:
            today = timezone.now().date()
            date_str = today.strftime("%Y%m%d")
            last_batch_today = MaterialInward.objects.filter(
                created_at__date=today
            ).count()
            batch_number = last_batch_today + 1
            self.batch = f"BATCH-{date_str}-{batch_number:03d}"

        # # Auto-fill ALL material details from Material master
        # if self.material_master:
        #     self.material_code = self.material_master.material_code
        #     self.material_name = self.material_master.material_name
        #     self.uom = self.material_master.uom
        #     self.category = self.material_master.category
            
            # # Auto-fill model, brand, and HSN code
            # self.model = self.material_master.model
            # self.brand = self.material_master.brand
            
            # # Get HSN code from material master
            # try:
            #     self.hsn_code = HSNCode.objects.get(hsn_code=self.material_master.hsn_code)
            # except HSNCode.DoesNotExist:
            #     # Create HSN code if it doesn't exist
            #     self.hsn_code = HSNCode.objects.create(hsn_code=self.material_master.hsn_code)

        # Auto-fill vendor name from Supplier
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.vendor_name

        super().save(*args, **kwargs)

    def clean(self):
        """Additional validation"""
        if self.invoice_date > timezone.now().date():
            raise ValidationError("Invoice date cannot be in the future")
        
        if self.grn_date > timezone.now().date():
            raise ValidationError("GRN date cannot be in the future")
            
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero")

    def __str__(self):
        return f"{self.grn_number} - {self.material_name} - Qty: {self.quantity}"



