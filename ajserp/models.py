from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User




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

    def save(self, *args, **kwargs):
        if not self.warehouse_code:
            # Generate warehouse code like: WH001, WH002, etc.
            last_warehouse = Warehouse.objects.order_by('warehouse_code').last()
            if last_warehouse:
                try:
                    # Extract number from "WH001" -> 1
                    last_number = int(last_warehouse.warehouse_code[2:])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.warehouse_code = f"WH{new_number:03d}"  # WH001, WH002, etc.
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.customer_code:
            # Generate customer code like: CU001, CU002, etc.
            last_customer = Customer.objects.order_by('customer_code').last()
            if last_customer:
                try:
                    # Extract number from "CU001" -> 1
                    last_number = int(last_customer.customer_code[2:])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.customer_code = f"CU{new_number:03d}"  # CU001, CU002, etc.
        super().save(*args, **kwargs)

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

    # Category is no longer the primary key
    category = models.CharField(
        max_length=20,
        choices=[
            ('Service', 'Service'),
            ('Spare', 'Spare'),
            ('Material', 'Material'),
        ]
    )

    # Material Code is now the UNIQUE & PRIMARY KEY
    material_code = models.CharField(max_length=50, primary_key=True)

    material_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=50)

    # You can convert to FK later — now we keep as it is
    hsn_code = models.CharField(max_length=10)

    # Pricing fields
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    price_from_date = models.DateField(null=True, blank=True)
    price_to_date = models.DateField(null=True, blank=True)
    pricing_status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
        ],
        default='Active'
    )

    # Model FK
    model = models.ForeignKey(
        MaterialModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='name',
        db_column='model_name'
    )

    # Brand FK
    brand = models.ForeignKey(
        MaterialBrand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='name',
        db_column='brand_name'
    )

    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    active_status = models.BooleanField(default=True)

    # AUTO-GENERATION OF MATERIAL CODE
    def save(self, *args, **kwargs):

        # If material_code not yet assigned, generate now
        if not self.material_code:

            # Your defined prefixes
            category_prefixes = {
                'Service': 'SESL',
                'Spare': 'SPSL',
                'Material': 'FGSL'
            }

            prefix = category_prefixes.get(self.category, 'MAT')

            # Find last code for the same category
            last_material = Material.objects.filter(
                material_code__startswith=prefix
            ).order_by('material_code').last()

            if last_material:
                try:
                    # Extract the numeric part
                    last_number = int(last_material.material_code[len(prefix):])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1

            # Final material_code
            self.material_code = f"{prefix}{new_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material_code} - {self.material_name}"

    
class PriceList(models.Model):
    PRICING_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    # FIXED: NOW THE FK LINKS TO material_code (UNIQUE)
    material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='prices',
        to_field='material_code',      # ← Correct
        db_column='material_code'      # ← Correct DB column name
    )

    # PRICES
    mrp_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # VALIDITY
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    
    # ACTIVE OR INACTIVE
    is_active = models.BooleanField(default=True)
    pricing_status = models.CharField(
        max_length=10, 
        choices=PRICING_STATUS_CHOICES, 
        default='Active'
    )
    
    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['material', 'from_date']   # Good & correct
        ordering = ['-from_date']
    
    def save(self, *args, **kwargs):
        today = timezone.now().date()
        
        # AUTOMATIC STATUS LOGIC
        if self.from_date > today:
            self.pricing_status = 'Inactive'
            self.is_active = False
        elif self.to_date and self.to_date < today:
            self.pricing_status = 'Inactive'
            self.is_active = False
        else:
            self.pricing_status = 'Active'
            self.is_active = True

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

class Estimate(models.Model):
    # Auto-generated fields
    estimate_number = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic information
    date = models.DateField(default=timezone.now)
    valid_till = models.DateField()
    ref_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Foreign Keys
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        to_field='warehouse_code',
        db_column='warehouse_code',
        verbose_name="Warehouse"
    )
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        to_field='customer_code',
        db_column='customer_code',
        verbose_name="Customer"
    )
    
    created_by = models.ForeignKey(
        'auth.User',  # Django's built-in User model
        on_delete=models.CASCADE,
        verbose_name="Created By"
    )
    
    # Customer billing address (auto-filled but editable)
    billing_address1 = models.TextField()
    billing_address2 = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=10)
    
    # Totals
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    igst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cess = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    round_off = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Additional fields
    description = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Estimate"
        verbose_name_plural = "Estimates"
        ordering = ['-date', '-estimate_number']
    
    def save(self, *args, **kwargs):
        # Auto-generate estimate number
        if not self.estimate_number:
            last_estimate = Estimate.objects.order_by('-id').first()
            if last_estimate and last_estimate.estimate_number:
                try:
                    last_number = int(last_estimate.estimate_number[3:])  # Extract number from EST001
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.estimate_number = f"EST{new_number:05d}"  # EST00001, EST00002
        
        # Auto-set valid_till to 30 days from date if not set
        if not self.valid_till:
            self.valid_till = self.date + timezone.timedelta(days=30)
            
        # Auto-generate ref_number if not provided
        if not self.ref_number:
            self.ref_number = f"REF-{self.estimate_number}"
        
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        """Calculate all totals from estimate items"""
        items = self.estimate_items.all()
        
        taxable_amount = sum(item.amount for item in items)
        sgst_amount = sum(item.sgst_amount for item in items)
        cgst_amount = sum(item.cgst_amount for item in items)
        igst_amount = sum(item.igst_amount for item in items)
        cess_amount = sum(item.cess_amount for item in items)
        
        total_tax = sgst_amount + cgst_amount + igst_amount + cess_amount
        grand_total = taxable_amount + total_tax
        
        # Round off
        round_off = round(grand_total) - grand_total
        
        # Update fields
        self.taxable_amount = taxable_amount
        self.sgst = sgst_amount
        self.cgst = cgst_amount
        self.igst = igst_amount
        self.cess = cess_amount
        self.round_off = round_off
        self.grand_total = grand_total + round_off
        
        self.save()
    
    def __str__(self):
        return f"{self.estimate_number} - {self.customer.customer_name}"

class EstimateItem(models.Model):
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        related_name='estimate_items'
    )
    
    # Material details - ONLY what you need
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name="Material"
    )
    
    material_name = models.CharField(max_length=255)  # Keep only name
    
    # Pricing - Keep only what you need
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=1)
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Tax rates (from material's HSN code)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cess_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Calculated fields
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    igst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cess_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Sequence
    sequence = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Estimate Item"
        verbose_name_plural = "Estimate Items"
        ordering = ['sequence']
    
    def save(self, *args, **kwargs):
        # Auto-fill only material name (no uom, hsn_code, etc.)
        if self.material and not self.material_name:
            self.material_name = self.material.material_name
            
            # Get tax rates from material's HSN code
            try:
                tax_rate = Taxes.objects.get(hsn_code=self.material.hsn_code)
                self.sgst_rate = tax_rate.sgst
                self.cgst_rate = tax_rate.cgst
                self.igst_rate = tax_rate.igst
                self.cess_rate = tax_rate.cess
            except Taxes.DoesNotExist:
                pass
        
        # Calculate amount
        discounted_price = self.mrp - self.discount
        self.amount = self.quantity * discounted_price
        
        # Calculate tax amounts
        self.sgst_amount = (self.amount * self.sgst_rate) / 100
        self.cgst_amount = (self.amount * self.cgst_rate) / 100
        self.igst_amount = (self.amount * self.igst_rate) / 100
        self.cess_amount = (self.amount * self.cess_rate) / 100
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.material_name} - Qty: {self.quantity}"
    
class SalesOrder(models.Model):
    # Auto-generated fields
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic information
    date = models.DateField(default=timezone.now)
    delivery_date = models.DateField()
    ref_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Foreign Keys
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        to_field='warehouse_code',
        db_column='warehouse_code',
        verbose_name="Warehouse"
    )
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        to_field='customer_code',
        db_column='customer_code',
        verbose_name="Customer"
    )
    
    created_by = models.ForeignKey(
        'auth.User',  # Django's built-in User model
        on_delete=models.CASCADE,
        verbose_name="Created By"
    )
    
    # Customer billing address (auto-filled but editable)
    billing_address1 = models.TextField()
    billing_address2 = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=10)
    
    # Totals - Fixed: Changed from max_digits=5 to max_digits=15 for tax amounts
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sgst = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cgst = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    igst = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cess = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    round_off = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Additional fields
    description = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    # Sales Order specific fields
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    delivery_terms = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = "Sales Order"
        verbose_name_plural = "Sales Orders"
        ordering = ['-date', '-order_number']
    
    def save(self, *args, **kwargs):
        # Auto-generate order number
        if not self.order_number:
            last_order = SalesOrder.objects.order_by('-id').first()
            if last_order and last_order.order_number:
                try:
                    last_number = int(last_order.order_number[2:])  # Extract number from SO001
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.order_number = f"SO{new_number:05d}"  # SO00001, SO00002
        
        # Auto-set delivery_date to 7 days from date if not set
        if not self.delivery_date:
            self.delivery_date = self.date + timezone.timedelta(days=7)
            
        # Auto-generate ref_number if not provided
        if not self.ref_number:
            self.ref_number = f"REF-{self.order_number}"
        
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        """Calculate all totals from sales order items"""
        items = self.sales_order_items.all()
        
        taxable_amount = sum(item.amount for item in items)
        sgst_amount = sum(item.sgst_amount for item in items)
        cgst_amount = sum(item.cgst_amount for item in items)
        igst_amount = sum(item.igst_amount for item in items)
        cess_amount = sum(item.cess_amount for item in items)
        
        total_tax = sgst_amount + cgst_amount + igst_amount + cess_amount
        grand_total = taxable_amount + total_tax
        
        # Round off
        round_off = round(grand_total) - grand_total
        
        # Update fields
        self.taxable_amount = taxable_amount
        self.sgst = sgst_amount
        self.cgst = cgst_amount
        self.igst = igst_amount
        self.cess = cess_amount
        self.round_off = round_off
        self.grand_total = grand_total + round_off
        
        self.save()
    
    def __str__(self):
        return f"{self.order_number} - {self.customer.customer_name}"

class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name='sales_order_items'
    )
    
    # Material details
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name="Material"
    )
    
    material_name = models.CharField(max_length=255)
    
    # Pricing
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=1)
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Tax rates (from material's HSN code)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cess_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Calculated fields
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    igst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cess_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Sales Order specific fields
    delivered_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    balance_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Sequence
    sequence = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Sales Order Item"
        verbose_name_plural = "Sales Order Items"
        ordering = ['sequence']
    
    def save(self, *args, **kwargs):
        # Auto-fill material name
        if self.material and not self.material_name:
            self.material_name = self.material.material_name
            
            # Get tax rates from material's HSN code
            try:
                tax_rate = Taxes.objects.get(hsn_code=self.material.hsn_code)
                self.sgst_rate = tax_rate.sgst
                self.cgst_rate = tax_rate.cgst
                self.igst_rate = tax_rate.igst
                self.cess_rate = tax_rate.cess
            except Taxes.DoesNotExist:
                pass
        
        # Calculate amount
        discounted_price = self.mrp - self.discount
        self.amount = self.quantity * discounted_price
        
        # Calculate tax amounts
        self.sgst_amount = (self.amount * self.sgst_rate) / 100
        self.cgst_amount = (self.amount * self.cgst_rate) / 100
        self.igst_amount = (self.amount * self.igst_rate) / 100
        self.cess_amount = (self.amount * self.cess_rate) / 100
        
        # Calculate balance quantity
        self.balance_quantity = self.quantity - self.delivered_quantity
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.material_name} - Qty: {self.quantity}"
    
class SalesInvoice(models.Model):
    # Auto-generated fields
    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic information
    date = models.DateField(default=timezone.now)
    ref_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Foreign Keys
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        to_field='warehouse_code',
        db_column='warehouse_code',
        verbose_name="Warehouse"
    )
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        to_field='customer_code',
        db_column='customer_code',
        verbose_name="Customer"
    )
    
    created_by = models.ForeignKey(
        'auth.User',  # Django's built-in User model
        on_delete=models.CASCADE,
        verbose_name="Created By"
    )
    
    # Customer billing address (auto-filled but editable)
    billing_address1 = models.TextField()
    billing_address2 = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=10)
    
    # Totals
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sgst = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cgst = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    igst = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cess = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    round_off = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Additional fields
    description = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    # Sales Invoice specific fields
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    
    # Payment information
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    
    # Reference to Sales Order (optional)
    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sales Order"
    )
    
    class Meta:
        verbose_name = "Sales Invoice"
        verbose_name_plural = "Sales Invoices"
        ordering = ['-date', '-invoice_number']
    
    def save(self, *args, **kwargs):
        # Auto-generate invoice number
        if not self.invoice_number:
            last_invoice = SalesInvoice.objects.order_by('-id').first()
            if last_invoice and last_invoice.invoice_number:
                try:
                    last_number = int(last_invoice.invoice_number[2:])  # Extract number from SI001
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.invoice_number = f"SI{new_number:05d}"  # SI00001, SI00002

        # Auto-generate ref_number if not provided
        if not self.ref_number:
            self.ref_number = f"REF-{self.invoice_number}"

        # Save the SalesInvoice first
        super().save(*args, **kwargs)
        
        # ===== AUTO-CREATE CUSTOMER LEDGER ENTRY =====
        self.create_customer_ledger_entry()
    
    def create_customer_ledger_entry(self):
        """Create entry in CustomerLedger for the sales invoice"""
        try:
            # Check if ledger entry already exists
            if not CustomerLedger.objects.filter(document_number=self.invoice_number).exists():
                CustomerLedger.objects.create(
                    transaction_type='Invoice',  # ← This is important!
                    document_number=self.invoice_number,
                    date=self.date,
                    customer_code=self.customer.customer_code,
                    customer_name=self.customer.customer_name,
                    dr_amount=self.grand_total,  # ← Customer OWES this amount (DR)
                    cr_amount=0,                # ← No receipt yet
                    reference=self.ref_number,
                    mode_of_payment=None,       # No payment for invoices
                    payment_reference=None,     # No payment reference for invoices
                )
                print(f"✅ Created Customer Ledger entry: {self.invoice_number}")
            else:
                print(f"ℹ️ Customer Ledger entry already exists: {self.invoice_number}")
                
        except Exception as e:
            print(f"❌ Error creating Customer Ledger entry: {e}")
    
    def calculate_totals(self):
        """Calculate all totals from sales invoice items"""
        items = self.sales_invoice_items.all()
        
        taxable_amount = sum(item.amount for item in items)
        sgst_amount = sum(item.sgst_amount for item in items)
        cgst_amount = sum(item.cgst_amount for item in items)
        igst_amount = sum(item.igst_amount for item in items)
        cess_amount = sum(item.cess_amount for item in items)
        
        total_tax = sgst_amount + cgst_amount + igst_amount + cess_amount
        grand_total = taxable_amount + total_tax
        
        # Round off
        round_off = round(grand_total) - grand_total
        
        # Update fields
        self.taxable_amount = taxable_amount
        self.sgst = sgst_amount
        self.cgst = cgst_amount
        self.igst = igst_amount
        self.cess = cess_amount
        self.round_off = round_off
        self.grand_total = grand_total + round_off
        
        self.save()
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer.customer_name}"

class SalesInvoiceItem(models.Model):
    sales_invoice = models.ForeignKey(
        SalesInvoice,
        on_delete=models.CASCADE,
        related_name='sales_invoice_items'
    )
    
    # Material details
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name="Material"
    )
    
    material_name = models.CharField(max_length=255)
    
    # Pricing
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=1)
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Tax rates (from material's HSN code)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="SGST Rate %")
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="CGST Rate %")
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="IGST Rate %")
    cess_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Cess Rate %")
    
    # Calculated fields
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    igst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cess_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Sequence
    sequence = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Sales Invoice Item"
        verbose_name_plural = "Sales Invoice Items"
        ordering = ['sequence']
    
    def save(self, *args, **kwargs):
        # Auto-fill material name
        if self.material and not self.material_name:
            self.material_name = self.material.material_name
            
            # Get tax rates from material's HSN code
            try:
                tax_rate = Taxes.objects.get(hsn_code=self.material.hsn_code)
                self.sgst_rate = tax_rate.sgst
                self.cgst_rate = tax_rate.cgst
                self.igst_rate = tax_rate.igst
                self.cess_rate = tax_rate.cess
            except Taxes.DoesNotExist:
                pass
        
        # Calculate amount
        discounted_price = self.mrp - self.discount
        self.amount = self.quantity * discounted_price
        
        # Calculate tax amounts USING THE PERCENTAGE RATES
        self.sgst_amount = (self.amount * self.sgst_rate) / 100
        self.cgst_amount = (self.amount * self.cgst_rate) / 100
        self.igst_amount = (self.amount * self.igst_rate) / 100
        self.cess_amount = (self.amount * self.cess_rate) / 100
        
        super().save(*args, **kwargs)
    
    # ✅ OPTION 2 - PROPERTIES TO GET WAREHOUSE DETAILS
    @property
    def warehouse(self):
        """Get warehouse from parent SalesInvoice"""
        return self.sales_invoice.warehouse
    
    @property
    def warehouse_name(self):
        """Get warehouse name"""
        return self.sales_invoice.warehouse.warehouse_name if self.sales_invoice.warehouse else ""
    
    @property
    def warehouse_full_address(self):
        """Get complete warehouse address"""
        if self.sales_invoice.warehouse:
            warehouse = self.sales_invoice.warehouse
            return f"{warehouse.address1}, {warehouse.city}, {warehouse.state} - {warehouse.postal_code}"
        return ""
    
    @property
    def warehouse_contact_info(self):
        """Get warehouse contact details"""
        if self.sales_invoice.warehouse:
            warehouse = self.sales_invoice.warehouse
            return f"Mobile: {warehouse.contact_number} | GSTIN: {warehouse.gst_number} | Email: {warehouse.email_address}"
        return ""
    
    def __str__(self):
        return f"{self.material_name} - Qty: {self.quantity}"

class ClaimRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('query_raised', 'Query Raised'),
        ('paid', 'Paid'),
    ]
    
    TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('oil', 'Oil'),
        ('other', 'Other'),
    ]

    document_number = models.CharField(max_length=50, unique=True, editable=False)
    date = models.DateField(auto_now_add=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="claim_requests")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_claims')
    previous_advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_claim = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_reference = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Employee submission timestamp   
    employee_submitted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    # Manager action timestamps - SEPARATE FIELDS to preserve history
    manager_approved_at = models.DateTimeField(null=True, blank=True)
    manager_rejected_at = models.DateTimeField(null=True, blank=True)
    manager_query_raised_at = models.DateTimeField(null=True, blank=True)
    
    # Latest manager action timestamp (for quick access)
    manager_action_at = models.DateTimeField(null=True, blank=True)
    manager_action_remarks = models.TextField(blank=True)
    manager_action_type = models.CharField(max_length=20, blank=True, null=True)  # 'approved', 'rejected', 'query_raised'

    def save(self, *args, **kwargs):
        if not self.document_number:
            # Generate document number like CLM00001, CLM00002
            last_claim = ClaimRequest.objects.order_by('document_number').last()
            if last_claim:
                try:
                    last_number = int(last_claim.document_number[3:])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.document_number = f"CLM{new_number:05d}"
        
        # Set employee submission timestamp when creating new claim
        if not self.pk and not self.employee_submitted_at:
            self.employee_submitted_at = timezone.now()
            
        super().save(*args, **kwargs)

    def get_latest_manager_action(self):
        """Get the latest manager action with timestamp"""
        if self.manager_action_at:
            return {
                'action': self.manager_action_type,
                'timestamp': self.manager_action_at,
                'remarks': self.manager_action_remarks
            }
        return None

    #def _str_(self):
       # return self.document_number
    def _str_(self):
        return f"{self.document_number} - {self.requested_by.username}"

class ClaimRequestItem(models.Model):
    claim_request = models.ForeignKey(ClaimRequest, on_delete=models.CASCADE, related_name='items')
    type = models.CharField(max_length=20, choices=ClaimRequest.TYPE_CHOICES)
    uom = models.CharField(max_length=50, verbose_name="Unit of Measure")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True)
    document = models.FileField(upload_to='claim_documents/', blank=True, null=True)

    def _str_(self):
        return f"{self.claim_request.document_number}-{self.type}"
    
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Auto-generated fields
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic information
    date = models.DateField(default=timezone.now)
    valid_till = models.DateField()  # CHANGED from delivery_date to valid_till
    ref_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Foreign Keys
    vendor = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        to_field='vendor_code',
        db_column='vendor_code',
        verbose_name="Vendor"
    )
    
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        to_field='warehouse_code',
        db_column='warehouse_code',
        verbose_name="Warehouse"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Created By"
    )
    
    # Billing Address
    billing_address1 = models.TextField()  # CHANGED from CharField to TextField
    billing_address2 = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=10)
    
    # Totals
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cgst = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sgst = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    igst = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cess = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    round_off = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Additional fields
    description = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"
        ordering = ['-date', '-order_number']

    def save(self, *args, **kwargs):
        # Auto-generate order number
        if not self.order_number:
            last_order = PurchaseOrder.objects.order_by('-id').first()
            if last_order and last_order.order_number:
                try:
                    last_number = int(last_order.order_number[2:])  # Extract number from PO001
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.order_number = f"PO{new_number:05d}"  # PO00001, PO00002
        
        # Auto-set valid_till to 30 days from date if not set
        if not self.valid_till:
            self.valid_till = self.date + timezone.timedelta(days=30)
        
        super().save(*args, **kwargs)

    def calculate_totals(self):
        """Calculate all totals from purchase order items"""
        items = self.purchase_order_items.all()
        
        taxable_amount = sum(item.amount for item in items)
        cgst_amount = sum(item.cgst_amount for item in items)
        sgst_amount = sum(item.sgst_amount for item in items)
        igst_amount = sum(item.igst_amount for item in items)
        cess_amount = sum(item.cess_amount for item in items)
        
        total_tax = cgst_amount + sgst_amount + igst_amount + cess_amount
        grand_total = taxable_amount + total_tax
        
        # Round off
        round_off = round(grand_total) - grand_total
        
        # Update fields
        self.taxable_amount = taxable_amount
        self.cgst = cgst_amount
        self.sgst = sgst_amount
        self.igst = igst_amount
        self.cess = cess_amount
        self.round_off = round_off
        self.grand_total = grand_total + round_off
        
        self.save()

    def __str__(self):
        return f"{self.order_number} - {self.vendor.vendor_name}"
    
class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, 
        on_delete=models.CASCADE, 
        related_name='purchase_order_items'
    )
    
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name="Material"
    )
    
    material_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=1)  # Increased precision
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Increased precision
    
    # Tax rates
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cess_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Tax amounts
    cgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Increased precision
    sgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cess_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    sequence = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Purchase Order Item"
        verbose_name_plural = "Purchase Order Items"
        ordering = ['sequence']

    def save(self, *args, **kwargs):
        # Auto-fill material name
        if self.material and not self.material_name:
            self.material_name = self.material.material_name
            
            # Get tax rates from material's HSN code
            try:
                tax_rate = Taxes.objects.get(hsn_code=self.material.hsn_code)
                self.cgst_rate = tax_rate.cgst
                self.sgst_rate = tax_rate.sgst
                self.igst_rate = tax_rate.igst
                self.cess_rate = tax_rate.cess
            except Taxes.DoesNotExist:
                pass
        
        # Calculate amount
        discounted_price = self.mrp - self.discount
        self.amount = self.quantity * discounted_price
        
        # Calculate tax amounts
        self.cgst_amount = (self.amount * self.cgst_rate) / 100
        self.sgst_amount = (self.amount * self.sgst_rate) / 100
        self.igst_amount = (self.amount * self.igst_rate) / 100
        self.cess_amount = (self.amount * self.cess_rate) / 100
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material_name} - Qty: {self.quantity}"
    
class VendorLedger(models.Model):
    # ONLY the fields from your table
    transaction_type = models.CharField(max_length=20)  # Invoice/Payment
    document_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.now)
    vendor_code = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=255)
    dr_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cr_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True, null=True)  # Ref
    mode_of_payment = models.CharField(max_length=20, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'ajserp_vendorledger'
        ordering = ['date', 'document_number']

    def __str__(self):
        return f"{self.document_number} - {self.vendor_name}"
    
class VendorInvoice(models.Model):
    # Auto-generated document number
    document_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # Basic Information
    transaction_type = models.CharField(max_length=20)
    document_date = models.DateField(default=timezone.now)
    
    # Vendor Information (ForeignKey for autocomplete)
    vendor = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        to_field='vendor_code',
        db_column='vendor_code',
        verbose_name="Vendor"
    )
    vendor_name = models.CharField(max_length=255, editable=False)
    
    # Invoice Details
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.DateField()
    
    # Material/Service Details
    hsn_code = models.CharField(max_length=10)
    material_service_details = models.CharField(max_length=255)
    uom = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Address (will auto-fill from vendor)
    address1 = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    
    # Tax Information
    tax_type = models.CharField(max_length=10)
    cess_applicable = models.BooleanField(default=False)
    payment_terms = models.CharField(max_length=20)
    
    # Pricing and Calculations
    basic_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cess_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cess_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tds_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tds_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Additional Fields
    uploaded_images = models.ImageField(upload_to='vendor_invoices/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vendor Invoice"
        verbose_name_plural = "Vendor Invoices"
        ordering = ['-document_date', '-document_number']

    def save(self, *args, **kwargs):
        # Auto-generate document number
        if not self.document_number:
            last_invoice = VendorInvoice.objects.order_by('-id').first()
            if last_invoice and last_invoice.document_number:
                try:
                    last_number = int(last_invoice.document_number[3:])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.document_number = f"VIN{new_number:05d}"
        
        # Auto-fill vendor name and address when vendor is selected
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.vendor_name
            self.address1 = self.vendor.billing_address1
            self.address2 = self.vendor.billing_address2 or ""
        
        # Calculate totals
        self.calculate_totals()
        
        # Save the VendorInvoice first
        super().save(*args, **kwargs)
        
        # ===== AUTO-CREATE VENDOR LEDGER ENTRY =====
        self.create_vendor_ledger_entry()

    def calculate_totals(self):
        """Calculate all tax amounts and total amount"""
        try:
            # Calculate tax amounts based on tax type
            if self.tax_type.upper() == 'CGST':
                self.cgst_amount = (self.basic_amount * self.cgst_rate) / 100
                self.sgst_amount = (self.basic_amount * self.sgst_rate) / 100
                self.igst_amount = 0
            elif self.tax_type.upper() == 'IGST':
                self.igst_amount = (self.basic_amount * self.igst_rate) / 100
                self.cgst_amount = 0
                self.sgst_amount = 0
            
            # Calculate cess amount if applicable
            if self.cess_applicable:
                self.cess_amount = (self.basic_amount * self.cess_rate) / 100
            else:
                self.cess_amount = 0
            
            # Calculate TDS amount
            self.tds_amount = (self.basic_amount * self.tds_rate) / 100
            
            # Calculate total amount
            tax_total = self.cgst_amount + self.sgst_amount + self.igst_amount + self.cess_amount
            self.total_amount = self.basic_amount + tax_total - self.discount_amount - self.tds_amount
            
            # Ensure amounts are not negative
            self.total_amount = max(self.total_amount, 0)
            
        except (TypeError, ValueError) as e:
            print(f"Error calculating totals: {e}")
            self.total_amount = self.basic_amount or 0

    def create_vendor_ledger_entry(self):
        """Create entry in VendorLedger"""
        try:
            # Check if ledger entry already exists
            if not VendorLedger.objects.filter(document_number=self.document_number).exists():
                VendorLedger.objects.create(
                    transaction_type='Invoice',
                    document_number=self.document_number,
                    date=self.document_date,
                    vendor_code=self.vendor.vendor_code,
                    vendor_name=self.vendor_name,
                    dr_amount=0,  # Invoices have Dr=0
                    cr_amount=self.total_amount,  # Invoices have Cr=amount
                    reference=self.invoice_number,  # Ref = invoice number
                    mode_of_payment=None,  # No payment mode for invoices
                    payment_reference=None,  # No payment reference for invoices
                )
                print(f"✅ Created Vendor Ledger entry: {self.document_number}")
            else:
                print(f"ℹ️ Vendor Ledger entry already exists: {self.document_number}")
                
        except Exception as e:
            print(f"❌ Error creating Vendor Ledger entry: {e}")

    def __str__(self):
        return f"{self.document_number} - {self.vendor_name}"
    
class VendorPayment(models.Model):
    # Auto-generated fields
    payment_id = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic Information
    payment_type = models.CharField(max_length=20, default='vendor_payment')
    payment_date = models.DateField(default=timezone.now)
    
    # Vendor Information
    vendor = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        to_field='vendor_code',
        db_column='vendor_code',
        verbose_name="Vendor"
    )
    vendor_name = models.CharField(max_length=255, editable=False)
    
    # Document Information
    document_type = models.CharField(max_length=20, default='against_invoice')
    document_number = models.CharField(max_length=100, blank=True, null=True)
    vendor_invoice = models.CharField(max_length=100, blank=True, null=True)
    
    # Payment Details
    mode_of_payment = models.CharField(max_length=20)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    
    # Amount Fields (These are just for display, calculations come from ledger)
    due_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance_outstanding = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Additional Fields
    remarks = models.TextField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, default='draft')

    class Meta:
        verbose_name = "Vendor Payment"
        verbose_name_plural = "Vendor Payments"
        ordering = ['-payment_date', '-payment_id']

    def save(self, *args, **kwargs):
        # Auto-generate payment ID
        if not self.payment_id:
            last_payment = VendorPayment.objects.order_by('-id').first()
            if last_payment and last_payment.payment_id:
                try:
                    last_number = int(last_payment.payment_id[3:])  # Extract number from PAY001
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.payment_id = f"PAY{new_number:05d}"  # PAY00001, PAY00002
        
        # Auto-fill vendor name
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.vendor_name
            
        # Calculate balance outstanding FROM LEDGER (after this payment)
        if self.vendor:
            ledger_due_amount = self.get_due_amount_from_ledger()
            # Balance after this payment = Ledger due amount - current payment amount
            self.balance_outstanding = ledger_due_amount - self.payment_amount
            
        # Set status to completed when payment is made
        if self.payment_amount > 0 and self.status == 'draft':
            self.status = 'completed'
            
        super().save(*args, **kwargs)
        
        # Create ledger entry after saving
        if self.status == 'completed':
            self.create_ledger_entries()

    def create_ledger_entries(self):
        """Create ledger entries for the payment"""
        try:
            # Create payment ledger entry (Dr entry for vendor)
            VendorLedger.objects.create(
                transaction_type='Payment',
                document_number=self.payment_id,
                date=self.payment_date,
                vendor_code=self.vendor.vendor_code,
                vendor_name=self.vendor_name,
                dr_amount=self.payment_amount,  # Payment reduces liability (Dr)
                cr_amount=0,
                reference=self.document_number or self.payment_id,
                mode_of_payment=self.mode_of_payment,
                payment_reference=self.payment_reference,
            )
            print(f"✅ Created Vendor Ledger entry for payment: {self.payment_id}")
            
        except Exception as e:
            print(f"❌ Error creating ledger entries: {e}")

    def get_due_amount_from_ledger(self):
        """Calculate due amount from vendor ledger (BEFORE this payment)"""
        try:
            ledger_entries = VendorLedger.objects.filter(vendor_code=self.vendor.vendor_code)
            
            total_debit = sum(entry.dr_amount for entry in ledger_entries)
            total_credit = sum(entry.cr_amount for entry in ledger_entries)
            
            # Due amount = Total Credit (invoices) - Total Debit (payments)
            due_amount = total_credit - total_debit
            
            return max(due_amount, 0)  # Return 0 if negative
        except Exception as e:
            print(f"Error calculating due amount: {e}")
            return 0

    def get_balance_after_payment(self):
        """Get balance outstanding after this payment (from ledger)"""
        try:
            ledger_entries = VendorLedger.objects.filter(vendor_code=self.vendor.vendor_code)
            
            total_debit = sum(entry.dr_amount for entry in ledger_entries)
            total_credit = sum(entry.cr_amount for entry in ledger_entries)
            
            # Balance = Total Credit (invoices) - Total Debit (payments including this one)
            balance = total_credit - total_debit
            
            return balance
        except Exception as e:
            print(f"Error calculating balance: {e}")
            return 0

    def __str__(self):
        return f"{self.payment_id} - {self.vendor_name} - {self.payment_amount}"
    
class CustomerLedger(models.Model):
    transaction_type = models.CharField(max_length=20)  # No choices needed
    document_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.now)
    customer_code = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=255)
    dr_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cr_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True, null=True)
    mode_of_payment = models.CharField(max_length=20, blank=True, null=True)  # No choices
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'ajserp_customerledger'
        ordering = ['date', 'document_number']

    def __str__(self):
        return f"{self.document_number} - {self.customer_name}"
    
class CustomerReceipt(models.Model):
    # Auto-generated fields
    collection_id = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Collection Information
    collected_by = models.CharField(max_length=100)
    collection_date = models.DateField(default=timezone.now)
    
    # Customer Information
    customer_code = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=255)
    
    # Invoice Selection
    invoice_numbers = models.JSONField(default=list, blank=True)
    
    # Amount Fields
    total_outstanding = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    amount_collected = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance_outstanding = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Payment Details
    payment_method = models.CharField(max_length=20)  # No choices needed
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    
    # Additional Fields
    uploaded_images = models.ImageField(upload_to='customer_receipts/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, default='draft')

    class Meta:
        verbose_name = "Customer Receipt"
        verbose_name_plural = "Customer Receipts"
        ordering = ['-collection_date', '-collection_id']

    def save(self, *args, **kwargs):
        # Auto-generate collection ID
        if not self.collection_id:
            last_receipt = CustomerReceipt.objects.order_by('-id').first()
            if last_receipt and last_receipt.collection_id:
                try:
                    last_number = int(last_receipt.collection_id[3:])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.collection_id = f"COL{new_number:05d}"
        
        # Calculate total_outstanding from CustomerLedger
        if self.customer_code:
            self.total_outstanding = self.get_due_amount_from_ledger()
        
        # Calculate balance outstanding
        if self.amount_collected > 0:
            self.balance_outstanding = self.total_outstanding - self.amount_collected
            
        super().save(*args, **kwargs)
        
        # Create ledger entry
        if self.amount_collected > 0 and self.status != 'cancelled':
            self.create_ledger_entry()

    def get_due_amount_from_ledger(self):
        """Calculate due amount from CustomerLedger (BEFORE this receipt)"""
        try:
            ledger_entries = CustomerLedger.objects.filter(customer_code=self.customer_code)
            
            total_debit = sum(entry.dr_amount for entry in ledger_entries)
            total_credit = sum(entry.cr_amount for entry in ledger_entries)
            
            # Due amount = Total Debit (invoices) - Total Credit (receipts)
            due_amount = total_debit - total_credit
            
            return max(due_amount, 0)  # Return 0 if negative
        except Exception as e:
            print(f"Error calculating due amount: {e}")
            return 0

    def create_ledger_entry(self):
        """Create entry in CustomerLedger for the receipt"""
        try:
            CustomerLedger.objects.create(
                transaction_type='Receipt',
                document_number=self.collection_id,
                date=self.collection_date,
                customer_code=self.customer_code,
                customer_name=self.customer_name,
                dr_amount=0,
                cr_amount=self.amount_collected,
                reference=', '.join(self.invoice_numbers) if self.invoice_numbers else self.collection_id,
                mode_of_payment=self.payment_method,
                payment_reference=self.payment_reference,
            )
        except Exception as e:
            print(f"Error creating Customer Ledger entry: {e}")

    def __str__(self):
        return f"{self.collection_id} - {self.customer_name} - ₹{self.amount_collected}"
    
# Add these models to your existing models.py
class CombinedTracker(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
    ]

    WORK_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    tracker_no = models.CharField(max_length=50, unique=True)
    application_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    remark = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    customer_city = models.CharField(max_length=100, blank=True)

    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    # Mandatory for enabling checkout
    work_completed = models.CharField(
        max_length=5, choices=WORK_CHOICES, blank=True, null=True
    )

    work_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='work_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.assigned_to and self.status == 'pending':
            self.status = 'assigned'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracker_no} - {self.name}"



    
# Add this to your models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    report_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')
    operating = models.CharField(max_length=50, blank=True)  # In-office, Remote, etc.
    mobile = models.CharField(max_length=15, blank=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"