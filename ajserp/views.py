from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Material, Taxes, Warehouse, Customer,Supplier, SupplierGroup, SupplierCategory, CustomerGroup, CustomerCategory, MaterialModel, MaterialBrand,MaterialInward,PriceList,HSNCode
# from .forms import MaterialForm, TaxesForm, WarehouseForm,CustomerForm,SupplierForm,MaterialInwardForm,PriceSearchForm
from datetime import datetime 
from django.http import JsonResponse 
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("ajserp:dashboard")
        else:
            return render(request, "ajserpadmin/login.html", {"error": "Invalid credentials"})
    return render(request, "ajserpadmin/login.html")

# Create your views here.
@login_required
def index(request):
    user=request.user
    context={
        "user":user,
    }
    return render(request, 'ajserpadmin/dashboard.html',context)  

@login_required 
def allproducts(request):
    return render(request, "ajserpadmin/allproducts.html")

# @login_required
# def warehouse(request):
#     return render(request, 'ajserpadmin/warehouse.html')

@login_required
def icon_menu(request):
    return render(request, "ajserpadmin/icon-menu.html")

# @login_required
# def addcustomers(request):
#     return render(request, "ajserpadmin/addcustomers.html")

# @login_required
# def customers(request):
#     return render(request, "ajserpadmin/customers.html")

# @login_required
# def addgroups(request):
#     return render(request, "ajserpadmin/addgroups.html")

# @login_required
# def addmaterial(request):
#     return render(request, "ajserpadmin/addmaterial.html")

@login_required
def addpricelists(request):
    return render(request, "ajserpadmin/addpricelists.html")

# @login_required
# def addsupliers(request):
#     return render(request, "ajserpadmin/addsupliers.html")

# @login_required
# def addwarehouse(request):
#     return render(request, "ajserpadmin/addwarehouse.html")

# @login_required
# def material(request):
#     return render(request, "ajserpadmin/material.html")

@login_required
def fontawesomeicons(request):
    return render(request, "ajserpadmin/fontawesomeicons.html")



@login_required
def pricelists(request):
    return render(request, "ajserpadmin/pricelists.html")

# @login_required
# def supliers(request):
#     return render(request, "ajserpadmin/supliers.html")

@login_required
def estimate(request):
    return render(request, "ajserpadmin/estimate.html")

@login_required
def purchaseorder(request):
    return render(request, "ajserpadmin/purchaseorder.html")

@login_required
def purchasereturn(request):
    return render(request, "ajserpadmin/purchasereturn.html")

@login_required
def salesorders(request):
    return render(request, "ajserpadmin/salesorders.html")

@login_required
def salesinvoice(request):
    return render(request, "ajserpadmin/salesinvoice.html")

@login_required
def deliverychallans(request):
    return render(request, "ajserpadmin/deliverychallans.html")

@login_required
def salesreturn(request):
    return render(request, "ajserpadmin/salesreturn.html")

@login_required
def creditnote(request):
    return render(request, "ajserpadmin/creditnote.html")

@login_required
def expenses(request):
    return render(request, "ajserpadmin/expenses.html")

@login_required
def receipts(request):
    return render(request, "ajserpadmin/receipts.html")

@login_required
def paymentout(request):
    return render(request, "ajserpadmin/paymentout.html")

@login_required
def vendorinvoice(request):
    return render(request, "ajserpadmin/vendorinvoice.html")

@login_required
def addestimate(request):
    return render(request, "ajserpadmin/addestimate.html")

@login_required
def addexpense(request):
    return render(request, "ajserpadmin/addexpense.html")

@login_required
def addreceipts(request):
    return render(request, "ajserpadmin/addreceipts.html")

@login_required
def addpaymentsout(request):
    return render(request, "ajserpadmin/addpaymentsout.html")

@login_required
def addvendorinvoice(request):
    return render(request, "ajserpadmin/addvendorinvoice.html")

@login_required
def claimapproval(request):
    return render(request, "ajserpadmin/claimapproval.html")

@login_required
def claimrequest(request):
    return render(request, "ajserpadmin/claimrequest.html")

@login_required
def addclaimrequest(request):
    return render(request, "ajserpadmin/addclaimrequest.html")

# @login_required
# def materialinward(request):
#     return render(request, "ajserpadmin/materialinward.html")

# @login_required
# def addmaterialinward(request):
#     return render(request, "ajserpadmin/addmaterialinward.html")

@login_required
def addsalesinvoice(request):
    return render(request, "ajserpadmin/addsalesinvoice.html")

@login_required
def addsalesorders(request):
    return render(request, "ajserpadmin/addsalesorders.html")

# @login_required
# def taxmaster(request):
#     return render(request, "ajserpadmin/taxmaster.html")

@login_required
def user(request):
    return render(request, "ajserpadmin/user.html")

@login_required
def addpurchaseorder(request):
    return render(request, "ajserpadmin/addpurchaseorder.html")

@login_required
def addpurchasereturn(request):
    return render(request, "ajserpadmin/addpurchasereturn.html")

@login_required
def profile(request):
    return render(request, "ajserpadmin/profile.html")

@login_required
def report(request):
    return render(request, "ajserpadmin/report.html")

@login_required
def salesdashboard(request):
    return render(request, "ajserpadmin/salesdashboard.html")


@login_required
def taxmaster(request):
    taxes = Taxes.objects.select_related('hsn_code').all()
    hsn_codes = HSNCode.objects.all()
    
    if request.method == 'POST':
        hsn_code = request.POST.get('hsn_code')
        cgst = request.POST.get('cgst')
        sgst = request.POST.get('sgst')
        igst = request.POST.get('igst')
        cess = request.POST.get('cess')

        try:
            # Get HSN code object (primary key lookup)
            hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
            
            # Check if tax rate already exists for this HSN
            if Taxes.objects.filter(hsn_code=hsn_obj).exists():
                messages.error(request, f'Tax rate for HSN {hsn_code} already exists!')
            else:
                # Create tax rate with HSN ForeignKey
                tax = Taxes(
                    hsn_code=hsn_obj,  # ForeignKey object
                    cgst=cgst or 0,
                    sgst=sgst or 0,
                    igst=igst or 0,
                    cess=cess or 0
                )
                tax.save()
                messages.success(request, f'Tax rate for HSN {hsn_code} added successfully!')
                
        except HSNCode.DoesNotExist:
            messages.error(request, f'HSN Code {hsn_code} not found! Create HSN code first.')
        except Exception as e:
            messages.error(request, f'Error adding tax rate: {str(e)}')
        
        return redirect('ajserp:taxmaster')
    
    return render(request, 'ajserpadmin/taxmaster.html', {
        'taxes': taxes,
        'hsn_codes': hsn_codes
    })

@login_required
def edit_tax(request, tax_id):
    try:
        tax = Taxes.objects.get(id=tax_id)
        hsn_codes = HSNCode.objects.all()
        
        if request.method == 'POST':
            hsn_code = request.POST.get('hsn_code')
            cgst = request.POST.get('cgst')
            sgst = request.POST.get('sgst')
            igst = request.POST.get('igst')
            cess = request.POST.get('cess')
            
            try:
                # Get HSN code object
                hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
                
                # Check if HSN code already exists (excluding current record)
                if Taxes.objects.filter(hsn_code=hsn_obj).exclude(id=tax_id).exists():
                    messages.error(request, f'Tax rate for HSN {hsn_code} already exists!')
                else:
                    tax.hsn_code = hsn_obj
                    tax.cgst = cgst or 0
                    tax.sgst = sgst or 0
                    tax.igst = igst or 0
                    tax.cess = cess or 0
                    tax.save()
                    
                    messages.success(request, f'Tax rate for HSN {hsn_code} updated successfully!')
                
            except HSNCode.DoesNotExist:
                messages.error(request, f'HSN Code {hsn_code} not found!')
            
            return redirect('ajserp:taxmaster')
        
        return render(request, 'ajserpadmin/edit_tax.html', {
            'tax': tax,
            'hsn_codes': hsn_codes
        })
    
    except Taxes.DoesNotExist:
        messages.error(request, 'Tax record not found!')
        return redirect('ajserp:taxmaster')

@login_required
def delete_tax(request, tax_id):
    if request.method == 'POST':
        try:
            tax = Taxes.objects.get(id=tax_id)
            hsn_code = tax.hsn_code.hsn_code
            tax.delete()
            messages.success(request, f'Tax rate for HSN {hsn_code} deleted successfully!')
        except Taxes.DoesNotExist:
            messages.error(request, 'Tax record not found!')
        except Exception as e:
            messages.error(request, f'Error deleting tax: {str(e)}')
    
    return redirect('ajserp:taxmaster')

@login_required
def get_hsn_suggestions(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # ✅ CORRECT: Search HSNCode model, not taxmaster
        hsn_data = HSNCode.objects.filter(hsn_code__icontains=query)[:10]
        results = [{'hsn_code': hsn.hsn_code} for hsn in hsn_data]
    return JsonResponse(results, safe=False)

@login_required
def addmaterial(request):
    print(f"🔍 ADD MATERIAL VIEW - Method: {request.method}")
    
    material_brands = MaterialBrand.objects.all()
    material_models = MaterialModel.objects.all()
    hsn_codes = HSNCode.objects.all()
    
    # Get selected HSN code from URL parameter
    selected_hsn = request.GET.get('selected_hsn', '')
    
    if request.method == 'POST':
        print("=" * 50)
        print("🚀 FORM SUBMISSION DEBUG INFO")
        print("=" * 50)
        print("✅ POST data received:", dict(request.POST))
        
        # Get all form data
        category = request.POST.get('category')
        material_name = request.POST.get('material_name')
        uom = request.POST.get('uom')
        model_name = request.POST.get('model')
        brand_name = request.POST.get('brand')
        description = request.POST.get('description')
        hsn_code = request.POST.get('hsn_code') or selected_hsn
        active_status = request.POST.get('active_status')
        
        print(f"📋 FORM FIELD VALUES:")
        print(f"  - Category: '{category}' (type: {type(category)})")
        print(f"  - Material Name: '{material_name}'")
        print(f"  - UOM: '{uom}'")
        print(f"  - Model: '{model_name}'")
        print(f"  - Brand: '{brand_name}'")
        print(f"  - HSN Code from form: '{request.POST.get('hsn_code')}'")
        print(f"  - HSN Code from URL: '{selected_hsn}'")
        print(f"  - HSN Code final: '{hsn_code}'")
        print(f"  - Active Status: '{active_status}'")
        print(f"  - Description: '{description}'")

        # Validation
        errors = {}
        if not category or category == "Select Category":
            errors['category'] = 'Category is required'
            print("❌ CATEGORY ERROR: Category is required or still 'Select Category'")
        else:
            print("✅ CATEGORY: Valid")
            
        if not material_name:
            errors['material_name'] = 'Material name is required'
            print("❌ MATERIAL NAME ERROR: Material name is required")
        else:
            print("✅ MATERIAL NAME: Valid")
            
        if not uom or uom == "Select UOM":
            errors['uom'] = 'UOM is required'
            print("❌ UOM ERROR: UOM is required or still 'Select UOM'")
        else:
            print("✅ UOM: Valid")
            
        if not hsn_code:
            errors['hsn_code'] = 'HSN code is required'
            print("❌ HSN CODE ERROR: HSN code is required")
        else:
            print("✅ HSN CODE: Valid")

        # Check if category already exists
        if category and category != "Select Category":
            if Material.objects.filter(category=category).exists():
                errors['category'] = f'Material with category "{category}" already exists!'
                print(f"❌ CATEGORY EXISTS ERROR: Category '{category}' already exists in database")
            else:
                print(f"✅ CATEGORY AVAILABLE: Category '{category}' is available")

        print(f"🔍 VALIDATION RESULT: {len(errors)} errors found")
        for field, error in errors.items():
            print(f"   - {field}: {error}")

        if not errors:
            print("🎉 ALL VALIDATIONS PASSED - Attempting to save material...")
            try:
                # Handle optional foreign keys
                model = None
                if model_name and model_name != "":
                    try:
                        model = MaterialModel.objects.get(name=model_name)
                        print(f"✅ MODEL: Found - {model.name}")
                    except MaterialModel.DoesNotExist:
                        print(f"⚠️ MODEL: Not found for code '{model_name}'")
                
                brand = None
                if brand_name and brand_name != "":
                    try:
                        brand = MaterialBrand.objects.get(name=brand_name)
                        print(f"✅ BRAND: Found - {brand.name}")
                    except MaterialBrand.DoesNotExist:
                        print(f"⚠️ BRAND: Not found for code '{brand_name}'")
                
                # Fix active_status handling
                active_status_bool = active_status == 'True'
                print(f"✅ ACTIVE STATUS: Converted '{active_status}' to {active_status_bool}")
                
                print(f"💾 CREATING MATERIAL OBJECT:")
                print(f"   - Category: {category}")
                print(f"   - Material Name: {material_name}") 
                print(f"   - UOM: {uom}")
                print(f"   - HSN Code: {hsn_code}")
                print(f"   - Active: {active_status_bool}")
                print(f"   - Model: {model}")
                print(f"   - Brand: {brand}")
                print(f"   - Description: {description}")
                
                # Create material instance
                material = Material(
                    category=category,
                    hsn_code=hsn_code,
                    material_name=material_name,
                    uom=uom,
                    model=model,
                    brand=brand,
                    description=description,
                    active_status=active_status_bool
                )
                
                print("💾 SAVING MATERIAL...")
                material.save()
                print(f"🎉 MATERIAL SAVED SUCCESSFULLY!")
                print(f"   - Material Code: {material.material_code}")
                print(f"   - Material ID: {material.category}")
                    
                messages.success(request, f'Material created successfully! Material Code: {material.material_code}')
                print("🔄 REDIRECTING to material list...")
                return redirect('ajserp:material')

            except Exception as e:
                print(f"💥 ERROR SAVING MATERIAL: {str(e)}")
                import traceback
                print(f"💥 TRACEBACK: {traceback.format_exc()}")
                messages.error(request, f"Error creating material: {str(e)}")
        else:
            print("❌ VALIDATION FAILED - Not saving material")
            for field, error in errors.items():
                messages.error(request, f"{field}: {error}")
        
        print("=" * 50)
        print("🔄 RENDERING FORM AGAIN (due to errors)")
        print("=" * 50)

    return render(request, 'ajserpadmin/addmaterial.html', {
        'material_brands': material_brands,
        'material_models': material_models,
        'hsn_codes': hsn_codes,
        'selected_hsn_code': selected_hsn
    })
    
@login_required
def material_suggestions(request):
    """API for material search suggestions"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in multiple fields
    materials = Material.objects.filter(
        Q(material_code__icontains=query) | 
        Q(material_name__icontains=query) |
        Q(category__icontains=query) |
        Q(uom__icontains=query) |
        Q(hsn_code__icontains=query)
    ).values('material_code', 'material_name', 'category', 'uom', 'hsn_code')[:10]
    
    return JsonResponse(list(materials), safe=False)

@login_required
def material_name_suggestions(request):
    """API for material name suggestions only"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    materials = Material.objects.filter(
        material_name__icontains=query
    ).values('material_name').distinct()[:10]
    
    # Return just the names as strings
    names = [material['material_name'] for material in materials]
    return JsonResponse(names, safe=False)
    
@login_required
def material(request):
    materials = Material.objects.select_related('model', 'brand','current_price').all()
    material_brands = MaterialBrand.objects.all()
    material_models = MaterialModel.objects.all()
    
     # ADD THIS - Get active price lists for dropdown in edit modal
    price_lists = PriceList.objects.filter(is_active=True)
    
    # Handle search filters
    if request.method == 'GET':
        # General search
        search_query = request.GET.get('q', '')
        if search_query:
            materials = materials.filter(
                Q(material_code__icontains=search_query) |
                Q(material_name__icontains=search_query) |
                Q(category__icontains=search_query) |
                Q(uom__icontains=search_query) |
                Q(hsn_code__icontains=search_query)
            )
        
        # Advanced filters
        material_name = request.GET.get('material_name')
        if material_name:
            materials = materials.filter(material_name__icontains=material_name)
        
        category = request.GET.get('category')
        if category:
            materials = materials.filter(category=category)
        
        brand_name = request.GET.get('brand')
        if brand_name:
            materials = materials.filter(brand__name=brand_name)
        
        status = request.GET.get('status')
        if status:
            if status == 'Active':
                materials = materials.filter(active_status=True)
            elif status == 'Inactive':
                materials = materials.filter(active_status=False)
    
    context = {
        'materials': materials,
        'material_brands': material_brands,
        'material_models': material_models,
        'search_params': request.GET
    }
    return render(request, 'ajserpadmin/material.html', context)

@login_required
def edit_material(request, category):
    try:
        material = Material.objects.get(category=category)
        material_brands = MaterialBrand.objects.all()
        material_models = MaterialModel.objects.all()
        hsn_codes = HSNCode.objects.all()
        price_lists = PriceList.objects.filter(is_active=True)  # ADD THIS
        
        if request.method == 'POST':
            category = request.POST.get('category')
            material_name = request.POST.get('material_name')
            uom = request.POST.get('uom')
            model_name = request.POST.get('model')
            brand_name = request.POST.get('brand')
            description = request.POST.get('description')
            hsn_code = request.POST.get('hsn_code')
            active_status = request.POST.get('active_status') == 'on'
            current_price_id = request.POST.get('current_price')  # ADD THIS
            
            errors = {}
            if not category:
                errors['category'] = 'Category is required'
            if not material_name:
                errors['material_name'] = 'Material name is required'
            if not uom:
                errors['uom'] = 'UOM is required'
            
            if category != material.category and Material.objects.filter(category=category).exists():
                errors['category'] = f'Material with category "{category}" already exists!'
            
            if not errors:
                try:
                    model = MaterialModel.objects.get(name=model_name) if model_name else None
                    brand = MaterialBrand.objects.get(name=brand_name) if brand_name else None
                    
                    # UPDATE CURRENT PRICE IF PROVIDED
                    if current_price_id:
                        try:
                            current_price = PriceList.objects.get(id=current_price_id)
                            material.current_price = current_price
                        except PriceList.DoesNotExist:
                            messages.warning(request, 'Selected price list not found')
                    
                    material.category = category
                    material.material_name = material_name
                    material.uom = uom
                    material.model = model
                    material.brand = brand
                    material.description = description
                    material.hsn_code = hsn_code
                    material.active_status = active_status
                    
                    material.save()
                    
                    messages.success(request, f'Material {material.material_code} updated successfully!')
                    return redirect('ajserp:material')
                    
                except Exception as e:
                    messages.error(request, f'Error updating material: {str(e)}')
            else:
                for error in errors.values():
                    messages.error(request, error)
        
        # UPDATE CONTEXT TO INCLUDE PRICE_LISTS
        context = {
            'material': material,
            'material_brands': material_brands,
            'material_models': material_models,
            'hsn_codes': hsn_codes,
            'price_lists': price_lists,  # ADD THIS
        }
        return render(request, 'ajserpadmin/edit_material.html', context)
    
    except Material.DoesNotExist:
        messages.error(request, 'Material not found!')
        return redirect('ajserp:material')


@login_required
def delete_material(request, category):
    if request.method == 'POST':
        try:
            material = Material.objects.get(category=category)
            material_code = material.material_code
            material_name = material.material_name
            material.delete()
            messages.success(request, f'Material {material_code} - {material_name} deleted successfully!')
        except Material.DoesNotExist:
            messages.error(request, 'Material not found!')
        except Exception as e:
            messages.error(request, f'Error deleting material: {str(e)}')
    
    return redirect('ajserp:material')

    
@login_required
def create_hsn_code(request):
    """Create new HSN code (primary key only)"""
    if request.method == 'POST':
        hsn_code = request.POST.get('hsn_code')
        
        if not hsn_code:
            messages.error(request, 'HSN code is required!')
            return redirect('ajserp:addmaterial')
        
        try:
            # Check if HSN code already exists (primary key validation)
            if HSNCode.objects.filter(hsn_code=hsn_code).exists():
                messages.error(request, f'HSN Code {hsn_code} already exists!')
                return redirect('ajserp:addmaterial')
            
            # Create new HSN code (only primary key)
            HSNCode.objects.create(hsn_code=hsn_code)
            
            messages.success(request, f'HSN Code {hsn_code} created successfully!')
            return redirect(f'{reverse("ajserp:addmaterial")}?selected_hsn={hsn_code}')
            
        except Exception as e:
            messages.error(request, f'Error creating HSN code: {str(e)}')
    
    return redirect('ajserp:addmaterial')

@login_required
def select_hsn_code(request):
    """Select existing HSN code"""
    if request.method == 'POST':
        hsn_code = request.POST.get('hsn_code')
        
        if not hsn_code:
            messages.error(request, 'Please select an HSN code!')
            return redirect('ajserp:addmaterial')
        
        try:
            # Verify HSN code exists (primary key lookup)
            HSNCode.objects.get(hsn_code=hsn_code)
            messages.info(request, f'HSN Code {hsn_code} selected!')
            return redirect(f'{reverse("ajserp:addmaterial")}?selected_hsn={hsn_code}')
            
        except HSNCode.DoesNotExist:
            messages.error(request, f'HSN Code {hsn_code} does not exist!')
    
    return redirect('ajserp:addmaterial')

@login_required
def delete_hsn_code(request, hsn_code):
    """Delete HSN code (primary key deletion)"""
    if request.method == 'POST':
        try:
            hsn = HSNCode.objects.get(hsn_code=hsn_code)
            hsn.delete()
            messages.success(request, f'HSN Code {hsn_code} deleted successfully!')
        except HSNCode.DoesNotExist:
            messages.error(request, 'HSN Code not found!')
        except Exception as e:
            messages.error(request, f'Error deleting HSN code: {str(e)}')
    
    return redirect('ajserp:addmaterial')

@login_required
def warehouse(request):
    warehouses = Warehouse.objects.all()  # ADD THIS
    return render(request, 'ajserpadmin/warehouse.html', {'warehouses': warehouses})

# @login_required
# def addwarehouse(request):
#     if request.method == 'POST':
#         form = WarehouseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('ajserp:warehouse')
#     else:
#         form = WarehouseForm()
#     return render(request, 'ajserpadmin/addwarehouse.html', {'form': form})

@login_required
# def addwarehouse(request):
#     if request.method == 'POST':
#         form = WarehouseForm(request.POST)
#         print("✅ Form data received:", request.POST)  # ADD THIS
#         if form.is_valid():
#             form.save()
#             print("✅ Warehouse saved successfully!")  # ADD THIS
#             return redirect('ajserp:warehouse')
#         else:
#             print("❌ Form errors:", form.errors)  # ADD THIS
#     else:
#         form = WarehouseForm()
#     return render(request, 'ajserpadmin/addwarehouse.html', {'form': form})
def addwarehouse(request):
    if request.method == 'POST':
        # Direct form handling
        warehouse_code = request.POST.get('warehouse_code')
        warehouse_name = request.POST.get('warehouse_name')
        contact_number = request.POST.get('contact_number')
        email_address = request.POST.get('email_address')
        state_of_supply = request.POST.get('state_of_supply')
        gst_number = request.POST.get('gst_number')
        address1 = request.POST.get('address1')
        description = request.POST.get('description')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        
        # Custom validation
        errors = {}
        if not warehouse_code:
            errors['warehouse_code'] = 'Warehouse code is required'
        if not warehouse_name:
            errors['warehouse_name'] = 'Warehouse name is required'
        if Warehouse.objects.filter(warehouse_code=warehouse_code).exists():
            errors['warehouse_code'] = 'Warehouse code already exists'
        
        if not errors:
            try:
                warehouse = Warehouse(
                    warehouse_code=warehouse_code,
                    warehouse_name=warehouse_name,
                    contact_number=contact_number,
                    email_address=email_address,
                    state_of_supply=state_of_supply,
                    gst_number=gst_number,
                    address1=address1,
                    description=description,
                    city=city,
                    state=state,
                    country=country,
                    postal_code=postal_code
                )
                warehouse.save()
                messages.success(request, 'Warehouse created successfully!')
                return redirect('ajserp:warehouse')
            except Exception as e:
                messages.error(request, f'Error creating warehouse: {str(e)}')
        else:
            for error in errors.values():
                messages.error(request, error)
    
    return render(request, 'ajserpadmin/addwarehouse.html')

# Customer List View
@login_required
def customers(request):
    customers = Customer.objects.select_related('customer_group', 'category').all()
    return render(request, 'ajserpadmin/customers.html', {'customers': customers})

@login_required
# def addcustomers(request):
#     # Get data for dropdowns
#     customer_groups = CustomerGroup.objects.all()
#     customer_categories = CustomerCategory.objects.all()
    
#     if request.method == 'POST':
#         print("✅ Received POST data:", dict(request.POST))
#         print("✅ Checkbox value:", request.POST.get('same_as_billing'))
        
#         post_data = request.POST.copy()
#         same_as_billing = post_data.get('same_as_billing') == 'on'
#         print("✅ Same as billing:", same_as_billing)
        
#         if same_as_billing:
#             print("✅ Copying billing to shipping...")
#             # Copy billing to shipping
#             post_data['shipping_address1'] = post_data.get('billing_address1', '')
#             post_data['shipping_city'] = post_data.get('billing_city', '')
#             post_data['shipping_state'] = post_data.get('billing_state', '')
#             post_data['shipping_country'] = post_data.get('billing_country', '')
#             post_data['shipping_postal_code'] = post_data.get('billing_postal_code', '')
#             print("✅ After copying:", {k: v for k, v in post_data.items() if 'shipping' in k})
        
#         form = CustomerForm(post_data, request.FILES)
        
#         if form.is_valid():
#             # Get the form instance without saving yet
#             customer = form.save(commit=False)
            
#             # Generate customer code
#             last_customer = Customer.objects.order_by('customer_code').last()
#             if last_customer:
#                 try:
#                     last_number = int(last_customer.customer_code[2:])  # Extract number from "CG001"
#                     new_number = last_number + 1
#                 except (ValueError, IndexError):
#                     new_number = 1
#             else:
#                 new_number = 1
#             customer.customer_code = f"CG{new_number:03d}"  # CG001, CG002, etc.
            
#             # Now save with the auto-generated code
#             customer.save()
            
#             print(f"✅ Customer created with code: {customer.customer_code}")
#             return redirect('ajserp:customers')
#         else:
#             print("❌ Customer form errors:", form.errors)
#     else:
#         form = CustomerForm()
    
#     return render(request, 'ajserpadmin/addcustomers.html', {
#         'form': form,
#         'customer_groups': customer_groups,
#         'customer_categories': customer_categories
#     })
def addcustomers(request):
    customer_groups = CustomerGroup.objects.all()
    customer_categories = CustomerCategory.objects.all()
    
    if request.method == 'POST':
        # Direct form handling
        customer_name = request.POST.get('customer_name')
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        email_address = request.POST.get('email_address')
        customer_group_code = request.POST.get('customer_group')
        category_code = request.POST.get('category')
        same_as_billing = request.POST.get('same_as_billing') == 'on'
        
        # Custom validation
        errors = {}
        if not customer_name:
            errors['customer_name'] = 'Customer name is required'
        if not contact_person:
            errors['contact_person'] = 'Contact person is required'
        
        if not errors:
            try:
                # Get foreign key objects
                customer_group = CustomerGroup.objects.get(code=customer_group_code) if customer_group_code else None
                category = CustomerCategory.objects.get(code=category_code) if category_code else None
                
                # Generate customer code
                last_customer = Customer.objects.order_by('customer_code').last()
                if last_customer:
                    try:
                        last_number = int(last_customer.customer_code[2:])
                        new_number = last_number + 1
                    except (ValueError, IndexError):
                        new_number = 1
                else:
                    new_number = 1
                customer_code = f"CG{new_number:03d}"
                
                customer = Customer(
                    customer_code=customer_code,
                    customer_name=customer_name,
                    contact_person=contact_person,
                    contact_number=contact_number,
                    email_address=email_address,
                    customer_group=customer_group,
                    category=category,
                    # ... add all other fields
                    same_as_billing=same_as_billing
                )
                
                # Handle same_as_billing logic
                if same_as_billing:
                    customer.shipping_address1 = request.POST.get('billing_address1')
                    customer.shipping_city = request.POST.get('billing_city')
                    customer.shipping_state = request.POST.get('billing_state')
                    customer.shipping_country = request.POST.get('billing_country')
                    customer.shipping_postal_code = request.POST.get('billing_postal_code')
                else:
                    customer.shipping_address1 = request.POST.get('shipping_address1')
                    customer.shipping_city = request.POST.get('shipping_city')
                    customer.shipping_state = request.POST.get('shipping_state')
                    customer.shipping_country = request.POST.get('shipping_country')
                    customer.shipping_postal_code = request.POST.get('shipping_postal_code')
                
                customer.save()
                messages.success(request, f'Customer created successfully! Code: {customer_code}')
                return redirect('ajserp:customers')
                
            except Exception as e:
                messages.error(request, f'Error creating customer: {str(e)}')
        else:
            for error in errors.values():
                messages.error(request, error)
    
    return render(request, 'ajserpadmin/addcustomers.html', {
        'customer_groups': customer_groups,
        'customer_categories': customer_categories
    })



@login_required
def addgroups(request):
    # Get all existing groups for display
    supplier_groups = SupplierGroup.objects.all()
    supplier_categories = SupplierCategory.objects.all()
    customer_groups = CustomerGroup.objects.all()
    customer_categories = CustomerCategory.objects.all()
    material_models = MaterialModel.objects.all()
    material_brands = MaterialBrand.objects.all()
    
    # Combine all groups into one list for the template
    all_groups = []
    
    # Add Supplier Groups
    for group in supplier_groups:
        all_groups.append({
            'code': group.code,
            'grouping': 'Supplier Group',
            'name': group.name,
            'description': group.description,
            'action': ''  # Empty for action buttons
        })
    
    # Add Supplier Categories
    for group in supplier_categories:
        all_groups.append({
            'code': group.code,
            'grouping': 'Supplier Category', 
            'name': group.name,
            'description': group.description,
            'action': ''
        })
    
    # Add Customer Groups
    for group in customer_groups:
        all_groups.append({
            'code': group.code,
            'grouping': 'Customer Group',
            'name': group.name,
            'description': group.description,
            'action': ''
        })
    
    # Add Customer Categories
    for group in customer_categories:
        all_groups.append({
            'code': group.code,
            'grouping': 'Customer Category',
            'name': group.name,
            'description': group.description,
            'action': ''
        })
    
    # Add Material Models
    for model in material_models:
        all_groups.append({
            'code': model.name,
            'grouping': 'Material Model',
            'name': model.name,
            'description': model.description,
            'action': ''
        })
    
    # Add Material Brands
    for brand in material_brands:
        all_groups.append({
            'code': brand.name,
            'grouping': 'Material Brand',
            'name': brand.name,
            'description': brand.description,
            'action': ''
        })
    
    if request.method == 'POST':
        # Handle Supplier Group
        if 'add_supplier_group' in request.POST:
            name = request.POST.get('supplier_group_name')
            description = request.POST.get('supplier_group_desc')
            if name:
                try:
                    # Generate code for supplier group
                    last_group = SupplierGroup.objects.order_by('code').last()
                    if last_group:
                        try:
                            last_number = int(last_group.code[3:])
                            new_number = last_number + 1
                        except (ValueError, IndexError):
                            new_number = 1
                    else:
                        new_number = 1
                    
                    code = f"SUG{new_number:03d}"
                    
                    obj = SupplierGroup.objects.create(code=code, name=name, description=description)
                    messages.success(request, f'{obj.code} - {name} created successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating Supplier Group: {str(e)}')

        # Handle Supplier Category
        elif 'add_supplier_category' in request.POST:
            name = request.POST.get('supplier_category_name')
            description = request.POST.get('supplier_category_desc')
            if name:
                try:
                    # Generate code for supplier category
                    last_category = SupplierCategory.objects.order_by('code').last()
                    if last_category:
                        try:
                            last_number = int(last_category.code[3:])
                            new_number = last_number + 1
                        except (ValueError, IndexError):
                            new_number = 1
                    else:
                        new_number = 1
                    
                    code = f"SUC{new_number:03d}"
                    
                    obj = SupplierCategory.objects.create(code=code, name=name, description=description)
                    messages.success(request, f'{obj.code} - {name} created successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating Supplier Category: {str(e)}')

        # Handle Customer Group
        elif 'add_customer_group' in request.POST:
            name = request.POST.get('customer_group_name')
            description = request.POST.get('customer_group_desc')
            if name:
                try:
                    # Generate code for customer group
                    last_group = CustomerGroup.objects.order_by('code').last()
                    if last_group:
                        try:
                            last_number = int(last_group.code[3:])
                            new_number = last_number + 1
                        except (ValueError, IndexError):
                            new_number = 1
                    else:
                        new_number = 1
                    
                    code = f"CUG{new_number:03d}"
                    
                    obj = CustomerGroup.objects.create(code=code, name=name, description=description)
                    messages.success(request, f'{obj.code} - {name} created successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating Customer Group: {str(e)}')

        # Handle Customer Category
        elif 'add_customer_category' in request.POST:
            name = request.POST.get('customer_category_name')
            description = request.POST.get('customer_category_desc')
            if name:
                try:
                    # Generate code for customer category
                    last_category = CustomerCategory.objects.order_by('code').last()
                    if last_category:
                        try:
                            last_number = int(last_category.code[3:])
                            new_number = last_number + 1
                        except (ValueError, IndexError):
                            new_number = 1
                    else:
                        new_number = 1
                    
                    code = f"CUC{new_number:03d}"
                    
                    obj = CustomerCategory.objects.create(code=code, name=name, description=description)
                    messages.success(request, f'{obj.code} - {name} created successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating Customer Category: {str(e)}')

         # Handle Material Model
        elif 'add_material_model' in request.POST:
            name = request.POST.get('material_model_name')
            description = request.POST.get('material_model_desc')
            if name:
                try:
                    # ✅ Since name is the primary key, just check if it exists
                    if MaterialModel.objects.filter(name=name).exists():
                        messages.error(request, f'Material Model "{name}" already exists!')
                    else:
                        # ✅ Create with name as primary key (no code needed)
                        obj = MaterialModel.objects.create(name=name, description=description)
                        messages.success(request, f'Material Model "{name}" created successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating Material Model: {str(e)}')

        # Handle Material Brand
        elif 'add_material_brand' in request.POST:
            name = request.POST.get('material_brand_name')
            description = request.POST.get('material_brand_desc')
            if name:
                try:
                    # ✅ Since name is the primary key, just check if it exists
                    if MaterialBrand.objects.filter(name=name).exists():
                        messages.error(request, f'Material Brand "{name}" already exists!')
                    else:
                        # ✅ Create with name as primary key (no code needed)
                        obj = MaterialBrand.objects.create(name=name, description=description)
                        messages.success(request, f'Material Brand "{name}" created successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating Material Brand: {str(e)}') 

        # Redirect after POST to refresh the page with new data
        return redirect('ajserp:addgroups')
    
    # Pass the groups data to the template
    return render(request, "ajserpadmin/addgroups.html", {'groups': all_groups})

@login_required
def edit_group(request, group_type, group_code):
    # Handle group editing based on group_type
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        try:
            # Update based on group type
            if group_type == 'supplier-group':
                group = SupplierGroup.objects.get(code=group_code)
            elif group_type == 'supplier-category':
                group = SupplierCategory.objects.get(code=group_code)
            elif group_type == 'customer-group':
                group = CustomerGroup.objects.get(code=group_code)
            elif group_type == 'customer-category':
                group = CustomerCategory.objects.get(code=group_code)
            elif group_type == 'material-model':
                group = MaterialModel.objects.get(code=group_code)
            elif group_type == 'material-brand':
                group = MaterialBrand.objects.get(code=group_code)
            else:
                messages.error(request, 'Invalid group type!')
                return redirect('ajserp:addgroups')
            
            group.name = name
            group.description = description
            group.save()
            messages.success(request, f'{group.code} updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating group: {str(e)}')
    
    return redirect('ajserp:addgroups')

@login_required
def delete_group(request, group_type, group_code):
    # Handle group deletion based on group_type
    if request.method == 'POST':
        try:
            if group_type == 'supplier-group':
                group = SupplierGroup.objects.get(code=group_code)
            elif group_type == 'supplier-category':
                group = SupplierCategory.objects.get(code=group_code)
            elif group_type == 'customer-group':
                group = CustomerGroup.objects.get(code=group_code)
            elif group_type == 'customer-category':
                group = CustomerCategory.objects.get(code=group_code)
            elif group_type == 'material-model':
                group = MaterialModel.objects.get(code=group_code)
            elif group_type == 'material-brand':
                group = MaterialBrand.objects.get(code=group_code)
            else:
                messages.error(request, 'Invalid group type!')
                return redirect('ajserp:addgroups')
            
            group_name = group.name
            group.delete()
            messages.success(request, f'{group_name} deleted successfully!')
            
        except Exception as e:
            messages.error(request, f'Error deleting group: {str(e)}')
    
    return redirect('ajserp:addgroups')

@login_required
def edit_customer(request, customer_id):
    # Handle customer editing
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=customer_id)
            
            # Get the selected group and category codes
            customer_group_code = request.POST.get('customer_group')
            category_code = request.POST.get('category')
            
            # Convert codes to ForeignKey objects
            customer_group = CustomerGroup.objects.get(code=customer_group_code) if customer_group_code else None
            category = CustomerCategory.objects.get(code=category_code) if category_code else None
            
            # Update customer fields
            customer.customer_name = request.POST.get('customer_name')
            customer.contact_person = request.POST.get('contact_person')
            customer.contact_number = request.POST.get('contact_number')
            customer.email_address = request.POST.get('email_address')
            customer.alt_contact_no = request.POST.get('alt_contact_no')
            customer.customer_group = customer_group
            customer.category = category
            customer.gst_number = request.POST.get('gst_number')
            customer.pan_no = request.POST.get('pan_no')
            customer.credit_period = request.POST.get('credit_period') or 0
            customer.credit_limit = request.POST.get('credit_limit') or 0.00
            customer.state_of_supply = request.POST.get('state_of_supply')
            customer.billing_address1 = request.POST.get('billing_address1')
            customer.billing_address2 = request.POST.get('billing_address2')
            customer.billing_city = request.POST.get('billing_city')
            customer.billing_state = request.POST.get('billing_state')
            customer.billing_country = request.POST.get('billing_country')
            customer.billing_postal_code = request.POST.get('billing_postal_code')
            customer.shipping_address1 = request.POST.get('shipping_address1')
            customer.shipping_address2 = request.POST.get('shipping_address2')
            customer.shipping_city = request.POST.get('shipping_city')
            customer.shipping_state = request.POST.get('shipping_state')
            customer.shipping_country = request.POST.get('shipping_country')
            customer.shipping_postal_code = request.POST.get('shipping_postal_code')
            customer.same_as_billing = request.POST.get('same_as_billing') == 'on'
            
            # Handle same_as_billing address copying
            if customer.same_as_billing:
                customer.shipping_address1 = customer.billing_address1
                customer.shipping_address2 = customer.billing_address2
                customer.shipping_city = customer.billing_city
                customer.shipping_state = customer.billing_state
                customer.shipping_country = customer.billing_country
                customer.shipping_postal_code = customer.billing_postal_code
            
            # Handle image upload
            if 'image' in request.FILES:
                customer.image = request.FILES['image']
            
            customer.save()
            messages.success(request, f'{customer.customer_name} updated successfully!')
            
        except Customer.DoesNotExist:
            messages.error(request, 'Customer not found!')
        except CustomerGroup.DoesNotExist:
            messages.error(request, 'Selected Customer Group does not exist!')
        except CustomerCategory.DoesNotExist:
            messages.error(request, 'Selected Customer Category does not exist!')
        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
    
    return redirect('ajserp:customers')

@login_required
def delete_customer(request, customer_id):
    # Handle customer deletion
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=customer_id)
            customer_name = customer.customer_name
            customer.delete()
            messages.success(request, f'{customer_name} deleted successfully!')
            
        except Customer.DoesNotExist:
            messages.error(request, 'Customer not found!')
        except Exception as e:
            messages.error(request, f'Error deleting customer: {str(e)}')
    
    return redirect('ajserp:customers')

# Supplier List View
@login_required
def supliers(request):
    suppliers = Supplier.objects.select_related('supplier_group', 'category').all()
    return render(request, 'ajserpadmin/supliers.html', {'suppliers': suppliers})

@login_required
# def addsupliers(request):
#     # Get data for dropdowns
#     supplier_groups = SupplierGroup.objects.all()
#     supplier_categories = SupplierCategory.objects.all()
    
#     if request.method == 'POST':
#         print("✅ Received POST data:", dict(request.POST))
#         print("✅ Checkbox value:", request.POST.get('same_as_billing'))
        
#         post_data = request.POST.copy()
#         same_as_billing = post_data.get('same_as_billing') == 'on'
#         print("✅ Same as billing:", same_as_billing)
        
#         if same_as_billing:
#             print("✅ Copying billing to shipping...")
#             # Copy billing to shipping
#             post_data['shipping_address1'] = post_data.get('billing_address1', '')
#             post_data['shipping_city'] = post_data.get('billing_city', '')
#             post_data['shipping_state'] = post_data.get('billing_state', '')
#             post_data['shipping_country'] = post_data.get('billing_country', '')
#             post_data['shipping_postal_code'] = post_data.get('billing_postal_code', '')
#             print("✅ After copying:", {k: v for k, v in post_data.items() if 'shipping' in k})
        
#         form = SupplierForm(post_data, request.FILES)
        
#         if form.is_valid():
#             # Get the form instance without saving yet
#             supplier = form.save(commit=False)
            
#             # Generate vendor code
#             last_supplier = Supplier.objects.order_by('vendor_code').last()
#             if last_supplier:
#                 try:
#                     last_number = int(last_supplier.vendor_code[3:])  # Extract number from "VEN001"
#                     new_number = last_number + 1
#                 except (ValueError, IndexError):
#                     new_number = 1
#             else:
#                 new_number = 1
#             supplier.vendor_code = f"VEN{new_number:03d}"  # VEN001, VEN002, etc.
            
#             # Now save with the auto-generated code
#             supplier.save()
            
#             print(f"✅ Supplier created with code: {supplier.vendor_code}")
#             return redirect('ajserp:supliers')
#         else:
#             print("❌ Supplier form errors:", form.errors)
#     else:
#         form = SupplierForm()
    
#     return render(request, 'ajserpadmin/addsupliers.html', {
#         'form': form,
#         'supplier_groups': supplier_groups,
#         'supplier_categories': supplier_categories
#     })
def addsupliers(request):
    supplier_groups = SupplierGroup.objects.all()
    supplier_categories = SupplierCategory.objects.all()
    
    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        email_address = request.POST.get('email_address')
        supplier_group_code = request.POST.get('supplier_group')
        category_code = request.POST.get('category')
        same_as_billing = request.POST.get('same_as_billing') == 'on'
        
        errors = {}
        if not vendor_name:
            errors['vendor_name'] = 'Vendor name is required'
        if not contact_person:
            errors['contact_person'] = 'Contact person is required'
        
        if not errors:
            try:
                supplier_group = SupplierGroup.objects.get(code=supplier_group_code) if supplier_group_code else None
                category = SupplierCategory.objects.get(code=category_code) if category_code else None
                
                last_supplier = Supplier.objects.order_by('vendor_code').last()
                if last_supplier:
                    try:
                        last_number = int(last_supplier.vendor_code[3:])
                        new_number = last_number + 1
                    except (ValueError, IndexError):
                        new_number = 1
                else:
                    new_number = 1
                vendor_code = f"VEN{new_number:03d}"
                
                supplier = Supplier(
                    vendor_code=vendor_code,
                    vendor_name=vendor_name,
                    contact_person=contact_person,
                    contact_number=contact_number,
                    email_address=email_address,
                    supplier_group=supplier_group,
                    category=category,
                    gst_number=request.POST.get('gst_number'),
                    pan_no=request.POST.get('pan_no'),
                    credit_period=request.POST.get('credit_period') or 0,
                    credit_limit=request.POST.get('credit_limit') or 0.00,
                    state_of_supply=request.POST.get('state_of_supply'),
                    billing_address1=request.POST.get('billing_address1'),
                    billing_address2=request.POST.get('billing_address2'),
                    billing_city=request.POST.get('billing_city'),
                    billing_state=request.POST.get('billing_state'),
                    billing_country=request.POST.get('billing_country'),
                    billing_postal_code=request.POST.get('billing_postal_code'),
                    shipping_address1=request.POST.get('shipping_address1'),
                    shipping_address2=request.POST.get('shipping_address2'),
                    shipping_city=request.POST.get('shipping_city'),
                    shipping_state=request.POST.get('shipping_state'),
                    shipping_country=request.POST.get('shipping_country'),
                    shipping_postal_code=request.POST.get('shipping_postal_code'),
                    same_as_billing=same_as_billing
                )
                
                if same_as_billing:
                    supplier.shipping_address1 = request.POST.get('billing_address1')
                    supplier.shipping_city = request.POST.get('billing_city')
                    supplier.shipping_state = request.POST.get('billing_state')
                    supplier.shipping_country = request.POST.get('billing_country')
                    supplier.shipping_postal_code = request.POST.get('billing_postal_code')
                
                supplier.save()
                messages.success(request, f'Supplier created successfully! Code: {vendor_code}')
                return redirect('ajserp:supliers')
                
            except Exception as e:
                messages.error(request, f'Error creating supplier: {str(e)}')
        else:
            for error in errors.values():
                messages.error(request, error)
    
    return render(request, 'ajserpadmin/addsupliers.html', {
        'supplier_groups': supplier_groups,
        'supplier_categories': supplier_categories
    })

@login_required
def edit_supplier(request, supplier_id):
    # Handle supplier editing
    if request.method == 'POST':
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            
            # Get the selected group and category codes
            supplier_group_code = request.POST.get('supplier_group')
            category_code = request.POST.get('category')
            
            # Convert codes to ForeignKey objects
            supplier_group = SupplierGroup.objects.get(code=supplier_group_code) if supplier_group_code else None
            category = SupplierCategory.objects.get(code=category_code) if category_code else None
            
            # Update supplier fields
            supplier.vendor_name = request.POST.get('vendor_name')
            supplier.contact_person = request.POST.get('contact_person')
            supplier.contact_number = request.POST.get('contact_number')
            supplier.email_address = request.POST.get('email_address')
            supplier.alt_contact_no = request.POST.get('alt_contact_no')
            supplier.supplier_group = supplier_group
            supplier.category = category
            supplier.gst_number = request.POST.get('gst_number')
            supplier.pan_no = request.POST.get('pan_no')
            supplier.credit_period = request.POST.get('credit_period') or 0
            supplier.credit_limit = request.POST.get('credit_limit') or 0.00
            supplier.state_of_supply = request.POST.get('state_of_supply')
            supplier.billing_address1 = request.POST.get('billing_address1')
            supplier.billing_address2 = request.POST.get('billing_address2')
            supplier.billing_city = request.POST.get('billing_city')
            supplier.billing_state = request.POST.get('billing_state')
            supplier.billing_country = request.POST.get('billing_country')
            supplier.billing_postal_code = request.POST.get('billing_postal_code')
            supplier.shipping_address1 = request.POST.get('shipping_address1')
            supplier.shipping_address2 = request.POST.get('shipping_address2')
            supplier.shipping_city = request.POST.get('shipping_city')
            supplier.shipping_state = request.POST.get('shipping_state')
            supplier.shipping_country = request.POST.get('shipping_country')
            supplier.shipping_postal_code = request.POST.get('shipping_postal_code')
            supplier.same_as_billing = request.POST.get('same_as_billing') == 'on'
            
            # Handle same_as_billing address copying
            if supplier.same_as_billing:
                supplier.shipping_address1 = supplier.billing_address1
                supplier.shipping_address2 = supplier.billing_address2
                supplier.shipping_city = supplier.billing_city
                supplier.shipping_state = supplier.billing_state
                supplier.shipping_country = supplier.billing_country
                supplier.shipping_postal_code = supplier.billing_postal_code
            
            # Handle image upload
            if 'image' in request.FILES:
                supplier.image = request.FILES['image']
            
            supplier.save()
            messages.success(request, f'{supplier.vendor_name} updated successfully!')
            
        except Supplier.DoesNotExist:
            messages.error(request, 'Supplier not found!')
        except SupplierGroup.DoesNotExist:
            messages.error(request, 'Selected Supplier Group does not exist!')
        except SupplierCategory.DoesNotExist:
            messages.error(request, 'Selected Supplier Category does not exist!')
        except Exception as e:
            messages.error(request, f'Error updating supplier: {str(e)}')
    
    return redirect('ajserp:supliers')

@login_required
def delete_supplier(request, supplier_id):
    # Handle supplier deletion
    if request.method == 'POST':
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            vendor_name = supplier.vendor_name
            supplier.delete()
            messages.success(request, f'{vendor_name} deleted successfully!')
            
        except Supplier.DoesNotExist:
            messages.error(request, 'Supplier not found!')
        except Exception as e:
            messages.error(request, f'Error deleting supplier: {str(e)}')
    
    return redirect('ajserp:supliers')

# @login_required
# def materialinward(request):
#     material_inwards = MaterialInward.objects.select_related('vendor', 'model', 'brand', 'taxes').all()
#     return render(request, "ajserpadmin/materialinward.html", {'material_inwards': material_inwards}) 
@login_required
def materialinward(request):
    material_inwards = MaterialInward.objects.select_related('vendor', 'model', 'brand', 'hsn_code').all()
    vendors = Supplier.objects.all()  # ADD THIS LINE
    return render(request, "ajserpadmin/materialinward.html", {
        'material_inwards': material_inwards,
        'vendors': vendors  # ADD THIS LINE
    })

@login_required
def addmaterialinward(request):
    vendors = Supplier.objects.all()
    material_models = MaterialModel.objects.all()
    material_brands = MaterialBrand.objects.all()
    hsn_codes = HSNCode.objects.all()
    
    if request.method == 'POST':
        print("=== MATERIAL INWARD FORM SUBMISSION DEBUG ===")
        print("POST data received:", dict(request.POST))
        
        # ✅ SIMPLE: Get values directly from form
        material_code = request.POST.get('material_code')
        material_search = request.POST.get('material_search')  # This will have the material name
        vendor_search = request.POST.get('vendor_search')     # This will have the vendor name
        category = request.POST.get('category')
        grn_date = request.POST.get('grn_date')
        batch = request.POST.get('batch')
        vendor_code = request.POST.get('vendor_code')
        invoice_number = request.POST.get('invoice_number')
        invoice_date = request.POST.get('invoice_date')
        quantity = request.POST.get('quantity')
        uom = request.POST.get('uom')
        model_name = request.POST.get('model')
        brand_name = request.POST.get('brand')
        hsn_code_value = request.POST.get('hsn_code')
        
        # ✅ Use the search input values directly
        material_name = material_search
        vendor_name = vendor_search
        
        print(f"Material Name from form: {material_name}")
        print(f"Vendor Name from form: {vendor_name}")
        
        errors = {}
        if not material_code:
            errors['material_code'] = 'Material code is required'
        if not material_name:
            errors['material_search'] = 'Material name is required - please select from autocomplete'
        if not category:
            errors['category'] = 'Category is required'
        if not vendor_name:
            errors['vendor_search'] = 'Vendor name is required - please select from autocomplete'
        
        if not errors:
            try:
                # Get related objects
                vendor = Supplier.objects.get(vendor_code=vendor_code) if vendor_code else None
                model = MaterialModel.objects.get(name=model_name) if model_name else None
                brand = MaterialBrand.objects.get(name=brand_name) if brand_name else None
                hsn_code_obj = HSNCode.objects.get(hsn_code=hsn_code_value) if hsn_code_value else None
                
                # ✅ Create MaterialInward with the names from search inputs
                material_inward = MaterialInward(
                    category=category,
                    grn_date=grn_date,
                    vendor=vendor,
                    invoice_number=invoice_number,
                    invoice_date=invoice_date,
                    quantity=quantity,
                    material_code=material_code,
                    material_name=material_name,  # From material_search input
                    uom=uom,
                    model=model,
                    brand=brand,
                    hsn_code=hsn_code_obj,
                    vendor_name=vendor_name  # From vendor_search input
                )
                material_inward.save()
                
                messages.success(request, f'Material Inward created successfully! GRN: {material_inward.grn_number}')
                return redirect('ajserp:materialinward')
                
            except Exception as e:
                messages.error(request, f'Error creating material inward: {str(e)}')
                print(f"Error: {str(e)}")
        else:
            for error in errors.values():
                messages.error(request, error)
    
    return render(request, 'ajserpadmin/addmaterialinward.html', {
        'vendors': vendors,
        'material_models': material_models,
        'material_brands': material_brands,
        'hsn_codes': hsn_codes
    })


@login_required
def material_autocomplete(request):
    """API for material autocomplete with combined display"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in both material_code and material_name
    materials = Material.objects.filter(
        Q(material_code__icontains=query) | 
        Q(material_name__icontains=query)
    ).values(
        'material_code', 
        'material_name', 
        'uom', 
        'category',
        'model__name',  # Get model code
        'brand__name',  # Get brand code  
        'hsn_code'
    )[:10]
    
    # Format the data
    material_list = []
    for material in materials:
        material_list.append({
            'material_code': material['material_code'],
            'material_name': material['material_name'],
            'uom': material['uom'],
            'category': material['category'],
            'model_name': material['model__name'],
            'brand_name': material['brand__name'],
            'hsn_code': material['hsn_code'],
        })
    
    return JsonResponse(material_list, safe=False)

@login_required
def vendor_autocomplete(request):
    """API for vendor autocomplete with combined display"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in both vendor_code and vendor_name
    vendors = Supplier.objects.filter(
        Q(vendor_code__icontains=query) | 
        Q(vendor_name__icontains=query)
    ).values('vendor_code', 'vendor_name')[:10]
    
    return JsonResponse(list(vendors), safe=False)

@login_required
def edit_materialinward(request, inward_id):
    try:
        material_inward = MaterialInward.objects.get(id=inward_id)
        vendors = Supplier.objects.all()
        material_models = MaterialModel.objects.all()
        material_brands = MaterialBrand.objects.all()
        hsn_codes = HSNCode.objects.all()
        
        if request.method == 'POST':
            category = request.POST.get('category')
            grn_number = request.POST.get('grn_number')
            grn_date = request.POST.get('grn_date')
            batch = request.POST.get('batch')
            vendor_code = request.POST.get('vendor_code')  # ✅ Changed from 'vendor'
            material_search = request.POST.get('material_search')  # ✅ Get from search input
            vendor_search = request.POST.get('vendor_search')  # ✅ Get from search input
            invoice_number = request.POST.get('invoice_number')
            invoice_date = request.POST.get('invoice_date')
            quantity = request.POST.get('quantity')
            uom = request.POST.get('uom')
            model_name = request.POST.get('model')
            brand_name = request.POST.get('brand')
            hsn_code_value = request.POST.get('hsn_code')
            
            # ✅ Extract names from search inputs
            material_name = material_search
            vendor_name = vendor_search
            
            errors = {}
            if not category:
                errors['category'] = 'Category is required'
            if not grn_number:
                errors['grn_number'] = 'GRN number is required'
            if not material_search:  # ✅ Check search input
                errors['material_search'] = 'Material name is required'
            if not uom:
                errors['uom'] = 'UOM is required'
            if not vendor_search:  # ✅ Check search input
                errors['vendor_search'] = 'Vendor name is required'
            
            if not errors:
                vendor = Supplier.objects.get(vendor_code=vendor_code) if vendor_code else None
                model = MaterialModel.objects.get(code=model_name) if model_name else None
                brand = MaterialBrand.objects.get(code=brand_name) if brand_name else None
                hsn_code_obj = HSNCode.objects.get(hsn_code=hsn_code_value) if hsn_code_value else None
                
                material_inward.category = category
                material_inward.grn_number = grn_number
                material_inward.grn_date = grn_date
                material_inward.batch = batch
                material_inward.vendor = vendor
                material_inward.invoice_number = invoice_number
                material_inward.invoice_date = invoice_date
                material_inward.quantity = quantity
                material_inward.material_name = material_name  # ✅ From search input
                material_inward.uom = uom
                material_inward.model = model
                material_inward.brand = brand
                material_inward.hsn_code = hsn_code_obj
                material_inward.vendor_name = vendor_name  # ✅ From search input
                
                material_inward.save()
                messages.success(request, f'Material Inward updated successfully! GRN: {grn_number}')
                return redirect('ajserp:materialinward')
            else:
                for error in errors.values():
                    messages.error(request, error)
        
        return render(request, 'ajserpadmin/editmaterialinward.html', {
            'material_inward': material_inward,
            'vendors': vendors,
            'material_models': material_models,
            'material_brands': material_brands,
            'hsn_codes': hsn_codes
        })
    
    except MaterialInward.DoesNotExist:
        messages.error(request, 'Material Inward record not found!')
        return redirect('ajserp:materialinward')
# Delete Material Inward View
@login_required
def delete_materialinward(request, inward_id):
    if request.method == 'POST':
        try:
            material_inward = MaterialInward.objects.get(id=inward_id)
            grn_number = material_inward.grn_number
            material_inward.delete()
            messages.success(request, f'Material Inward {grn_number} deleted successfully!')
        except MaterialInward.DoesNotExist:
            messages.error(request, 'Material Inward record not found!')
        except Exception as e:
            messages.error(request, f'Error deleting Material Inward: {str(e)}')
    
    return redirect('ajserp:materialinward')

# def addpricelists(request):
#     search_form = PriceSearchForm(request.GET or None)
    
#     # Get ALL materials by default with related data
#     materials = Material.objects.select_related('model', 'brand', 'taxes').all()
    
#     # Handle search form submission
#     if request.method == 'GET' and any(key in request.GET for key in ['material_code', 'material_name', 'category', 'model', 'status']):
#         # Apply filters to materials
#         if 'material_code' in request.GET and request.GET['material_code']:
#             materials = materials.filter(material_code__icontains=request.GET['material_code'])
        
#         if 'material_name' in request.GET and request.GET['material_name']:
#             materials = materials.filter(material_name__icontains=request.GET['material_name'])
        
#         if 'category' in request.GET and request.GET['category']:
#             materials = materials.filter(category=request.GET['category'])
        
#         if 'model' in request.GET and request.GET['model']:
#             materials = materials.filter(model__name__icontains=request.GET['model'])
        
#         if 'brand' in request.GET and request.GET['brand']:
#             materials = materials.filter(brand__name__icontains=request.GET['brand'])
        
#         # Status filter
#         if 'status' in request.GET and request.GET['status']:
#             if request.GET['status'] == 'Active':
#                 materials = materials.filter(active_status=True)
#             elif request.GET['status'] == 'Inactive':
#                 materials = materials.filter(active_status=False)
                
#      # MRP Range filters
#         if request.GET.get('min_mrp'):
#             materials = materials.filter(mrp__gte=request.GET['min_mrp'])
        
#         if request.GET.get('max_mrp'):
#             materials = materials.filter(mrp__lte=request.GET['max_mrp'])
        
#         # Selling Price Range filters
#         if request.GET.get('min_selling_price'):
#             materials = materials.filter(selling_price__gte=request.GET['min_selling_price'])
        
#         if request.GET.get('max_selling_price'):
#             materials = materials.filter(selling_price__lte=request.GET['max_selling_price'])
        
#         # Exact Price filters
#         if request.GET.get('exact_mrp'):
#             materials = materials.filter(mrp=request.GET['exact_mrp'])
        
#         if request.GET.get('exact_selling_price'):
#             materials = materials.filter(selling_price=request.GET['exact_selling_price'])
    
#     # Handle price update form submission
#     elif request.method == 'POST':
#         updated_count = 0
        
#         # Get all material codes from the form
#         material_codes = request.POST.getlist('material_code')
#         mrp_prices = request.POST.getlist('mrp_price')
#         selling_prices = request.POST.getlist('selling_price')
#         from_dates = request.POST.getlist('from_date')
#         to_dates = request.POST.getlist('to_date')
#         statuses = request.POST.getlist('status')
        
#         for i, material_code in enumerate(material_codes):
#             try:
#                 material = Material.objects.get(material_code=material_code)
                
#                 # Get values from form
#                 mrp_price = mrp_prices[i] if i < len(mrp_prices) and mrp_prices[i] else 0
#                 selling_price = selling_prices[i] if i < len(selling_prices) and selling_prices[i] else 0
#                 from_date = from_dates[i] if i < len(from_dates) and from_dates[i] else None
#                 to_date = to_dates[i] if i < len(to_dates) and to_dates[i] else None
#                 is_active = statuses[i] == 'Active' if i < len(statuses) else True
                
#                 # Basic validation
#                 if selling_price and mrp_price and float(selling_price) > float(mrp_price):
#                     messages.warning(request, f"Selling price cannot be greater than MRP for {material_code}")
#                     continue
                
#                 if from_date and to_date and from_date > to_date:
#                     messages.warning(request, f"From date cannot be greater than To date for {material_code}")
#                     continue
                
#                 # Update or create price list entry
#                 price_list, created = PriceList.objects.get_or_create(
#                     material=material,
#                     defaults={
#                         'mrp_price': mrp_price,
#                         'selling_price': selling_price,
#                         'from_date': from_date,
#                         'to_date': to_date,
#                         'is_active': is_active
#                     }
#                 )
                
#                 if not created:
#                     # Update existing price list
#                     price_list.mrp_price = mrp_price
#                     price_list.selling_price = selling_price
#                     price_list.from_date = from_date
#                     price_list.to_date = to_date
#                     price_list.is_active = is_active
#                     price_list.save()
                
#                 updated_count += 1
                
#             except Material.DoesNotExist:
#                 messages.error(request, f"Material {material_code} not found")
#             except Exception as e:
#                 messages.error(request, f"Error updating material {material_code}: {str(e)}")
        
#         if updated_count > 0:
#             messages.success(request, f"Successfully updated prices for {updated_count} materials.")
#         else:
#             messages.warning(request, "No materials were updated.")
        
#         return redirect('ajserp:addpricelists')
    
#     context = {
#         'search_form': search_form,
#         'materials': materials,
#         'search_params': request.GET if request.GET else {}
#     }
    
#     return render(request, 'ajserpadmin/addpricelists.html', context)

@login_required
def addpricelists(request):
    materials = Material.objects.select_related('model', 'brand').all()
    
    # Handle search
    if request.method == 'GET':
        materials = apply_search_filters(materials, request.GET)
    
    # Handle price updates
    elif request.method == 'POST':
        updated_count = 0
        
        material_codes = request.POST.getlist('material_code')
        mrp_prices = request.POST.getlist('mrp_price')
        selling_prices = request.POST.getlist('selling_price')
        from_dates = request.POST.getlist('from_date')
        to_dates = request.POST.getlist('to_date')
        statuses = request.POST.getlist('status')
        
        for i, material_code in enumerate(material_codes):
            try:
                material = Material.objects.get(material_code=material_code)
                
                mrp_price = mrp_prices[i] if i < len(mrp_prices) and mrp_prices[i] else 0
                selling_price = selling_prices[i] if i < len(selling_prices) and selling_prices[i] else 0
                from_date = from_dates[i] if i < len(from_dates) and from_dates[i] else None
                to_date = to_dates[i] if i < len(to_dates) and to_dates[i] else None
                is_active = statuses[i] == 'Active' if i < len(statuses) else True
                
                # Validation
                if selling_price and mrp_price and float(selling_price) > float(mrp_price):
                    messages.warning(request, f"Selling price cannot be greater than MRP for {material_code}")
                    continue
                
                # Create or update PriceList
                price_list, created = PriceList.objects.get_or_create(
                    material=material,
                    defaults={
                        'mrp_price': mrp_price,
                        'selling_price': selling_price,
                        'from_date': from_date,
                        'to_date': to_date,
                        'is_active': is_active
                    }
                )
                
                if not created:
                    price_list.mrp_price = mrp_price
                    price_list.selling_price = selling_price
                    price_list.from_date = from_date
                    price_list.to_date = to_date
                    price_list.is_active = is_active
                    price_list.save()
                
                updated_count += 1
                
            except Exception as e:
                messages.error(request, f"Error updating {material_code}: {str(e)}")
        
        if updated_count > 0:
            messages.success(request, f"Updated {updated_count} materials")
        
        return redirect('ajserp:addpricelists')
    
    context = {
        'materials': materials,
        'search_params': request.GET if request.GET else {}
    }
    
    return render(request, 'ajserpadmin/addpricelists.html', context)

def apply_search_filters(materials, get_params):
    """Apply search filters to materials queryset"""
    if get_params.get('material_code'):
        materials = materials.filter(material_code__icontains=get_params['material_code'])
    
    if get_params.get('material_name'):
        materials = materials.filter(material_name__icontains=get_params['material_name'])
    
    if get_params.get('category'):
        materials = materials.filter(category=get_params['category'])
    
    if get_params.get('model'):
        materials = materials.filter(model__name__icontains=get_params['model'])
        
    if get_params.get('brand'):
        materials = materials.filter(brand__name__icontains=get_params['brand']) 
    
    if get_params.get('status'):
        if get_params['status'] == 'Active':
            materials = materials.filter(active_status=True)
        elif get_params['status'] == 'Inactive':
            materials = materials.filter(active_status=False)
    
    return materials

@login_required
def logout(request):
    auth_logout(request)
    return redirect("ajserp:login")





