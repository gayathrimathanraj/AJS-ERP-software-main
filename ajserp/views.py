from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Material, Taxes, Warehouse, Customer,Supplier, SupplierGroup, SupplierCategory, CustomerGroup, CustomerCategory, MaterialModel, MaterialBrand,MaterialInward,PriceList,HSNCode,Estimate,EstimateItem,ClaimRequest, ClaimRequestItem,SalesOrder, SalesOrderItem,SalesInvoice, SalesInvoiceItem,PurchaseOrder,PurchaseOrderItem,VendorInvoice,VendorPayment,VendorLedger, CustomerReceipt, CustomerLedger,Tracker,WorkSession, User,UserProfile
# from .forms import MaterialForm, TaxesForm, WarehouseForm,CustomerForm,SupplierForm,MaterialInwardForm,PriceSearchForm
from datetime import datetime 
from django.http import JsonResponse 
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
import json
from django.db import models
from django.db.models import Sum 
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from datetime import timedelta
from xhtml2pdf import pisa
from num2words import num2words
import os                                   
from django.conf import settings 
from django.http import HttpResponseBadRequest


 
  






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

# @login_required
# def addpricelists(request):
#     return render(request, "ajserpadmin/addpricelists.html")

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
    """Display list of all estimates"""
    estimates = Estimate.objects.all().order_by('-date').prefetch_related('estimate_items')
    
    # Get filter parameters
    estimate_number = request.GET.get('estimate_number', '')
    customer_name = request.GET.get('customer_name', '')
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    q = request.GET.get('q', '')  # Global search parameter
    
    # Apply filters
    if estimate_number:
        estimates = estimates.filter(estimate_number__icontains=estimate_number)
    if customer_name:
        estimates = estimates.filter(customer__customer_name__icontains=customer_name)
    if status:
        estimates = estimates.filter(status=status)
    if from_date:
        estimates = estimates.filter(date__gte=from_date)
    if to_date:
        estimates = estimates.filter(date__lte=to_date)
        
     # Global search (search across multiple fields)
    if q:
        estimates = estimates.filter(
            models.Q(estimate_number__icontains=q) |
            models.Q(customer__customer_name__icontains=q) |
            models.Q(billing_city__icontains=q) |
            models.Q(ref_number__icontains=q)
        )
        
    # Pagination - Show 10 estimates per page
    paginator = Paginator(estimates, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "ajserpadmin/estimate.html", {
        'estimates': page_obj,  # Changed from estimates to page_obj
        'customers': customers,
        'page_obj': page_obj,   # Add page_obj for pagination controls
    })
    
    

# @login_required
# def purchaseorder(request):
#     return render(request, "ajserpadmin/purchaseorder.html")

@login_required
def purchasereturn(request):
    return render(request, "ajserpadmin/purchasereturn.html")

# @login_required
# def salesorders(request):
#     return render(request, "ajserpadmin/salesorders.html")

# @login_required
# def salesinvoice(request):
#     return render(request, "ajserpadmin/salesinvoice.html")

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

# @login_required
# def addestimate(request):
#     return render(request, "ajserpadmin/addestimate.html")

@login_required
def addexpense(request):
    return render(request, "ajserpadmin/addexpense.html")

@login_required
def addreceipts(request):
    return render(request, "ajserpadmin/addreceipts.html")

# @login_required
# def addpaymentsout(request):
#     return render(request, "ajserpadmin/addpaymentsout.html")

@login_required
def addvendorinvoice(request):
    return render(request, "ajserpadmin/addvendorinvoice.html")

@login_required
def claimapproval(request):
    return render(request, "ajserpadmin/claimapproval.html")



# @login_required
# def materialinward(request):
#     return render(request, "ajserpadmin/materialinward.html")

# @login_required
# def addmaterialinward(request):
#     return render(request, "ajserpadmin/addmaterialinward.html")



# @login_required
# def addsalesorders(request):
#     return render(request, "ajserpadmin/addsalesorders.html")

# @login_required
# def taxmaster(request):
#     return render(request, "ajserpadmin/taxmaster.html")

@login_required
def user(request):
    users = User.objects.all().select_related('profile')
    return render(request, "ajserpadmin/user.html", {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        try:
            # Create User
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                designation=request.POST.get('designation', ''),
                department=request.POST.get('department', ''),
                location=request.POST.get('location', ''),
                operating=request.POST.get('operating', ''),
                mobile=request.POST.get('mobile', ''),
                remarks=request.POST.get('remarks', '')
            )
            
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return redirect('ajserp:user')

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        try:
            # Update User
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            
            # Update UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.designation = request.POST.get('designation', '')
            profile.department = request.POST.get('department', '')
            profile.location = request.POST.get('location', '')
            profile.operating = request.POST.get('operating', '')
            profile.mobile = request.POST.get('mobile', '')
            profile.remarks = request.POST.get('remarks', '')
            profile.save()
            
            messages.success(request, 'User updated successfully!')
            return redirect('user')
            
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return redirect('user')

@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, 'User deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('user')

# @login_required
# def addpurchaseorder(request):
#     return render(request, "ajserpadmin/addpurchaseorder.html")

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
        
        if request.method == 'POST':
            cgst = request.POST.get('cgst')
            sgst = request.POST.get('sgst')
            igst = request.POST.get('igst')
            cess = request.POST.get('cess')
            
            print(f"🔍 EDIT TAX DEBUG - CGST: {cgst}, SGST: {sgst}, IGST: {igst}, CESS: {cess}")
            
            # Update the tax record (keep same HSN code, only update tax rates)
            tax.cgst = float(cgst) if cgst else 0
            tax.sgst = float(sgst) if sgst else 0
            tax.igst = float(igst) if igst else 0
            tax.cess = float(cess) if cess else 0
            tax.save()
            
            print(f"✅ TAX UPDATED - HSN: {tax.hsn_code.hsn_code}, CGST: {tax.cgst}, SGST: {tax.sgst}")
            messages.success(request, f'Tax rate for HSN {tax.hsn_code.hsn_code} updated successfully!')
            return redirect('ajserp:taxmaster')
        
        # For GET request, show the edit form
        context = {
            'tax': tax
        }
        return render(request, 'ajserpadmin/edit_tax.html', context)
    
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
def get_hsn_codes_with_taxes(request):
    """API to get all HSN codes with their tax rates for the popup modal"""
    hsn_codes = HSNCode.objects.all().order_by('hsn_code')
    
    result = []
    for hsn in hsn_codes:
        try:
            tax = Taxes.objects.get(hsn_code=hsn)
            tax_data = {
                'hsn_code': hsn.hsn_code,
                'cgst': str(tax.cgst),
                'sgst': str(tax.sgst),
                'igst': str(tax.igst),
                'cess': str(tax.cess),
                'has_tax': True,
                'created_at': tax.created_at.strftime("%d/%m/%Y")
            }
        except Taxes.DoesNotExist:
            tax_data = {
                'hsn_code': hsn.hsn_code,
                'cgst': '-',
                'sgst': '-', 
                'igst': '-',
                'cess': '-',
                'has_tax': False,
                'created_at': hsn.created_at.strftime("%d/%m/%Y")
            }
        
        result.append(tax_data)
    
    return JsonResponse(result, safe=False)

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
    
    print(f"🔍 MATERIAL NAME SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        print("❌ Query too short, returning empty")
        return JsonResponse([], safe=False)
    
    # OPTION 2: Using values() correctly
    materials = Material.objects.filter(
        material_name__icontains=query
    ).values('material_name').distinct()[:10]
    
    # Convert QuerySet to list of strings
    names_list = [item['material_name'] for item in materials]
    print(f"✅ Found {len(names_list)} materials: {names_list}")
    
    return JsonResponse(names_list, safe=False)
# def material_name_suggestions(request):
#     """API for material name suggestions only"""
#     query = request.GET.get('q', '').strip()
    
#     if len(query) < 2:
#         return JsonResponse([], safe=False)
    
#     materials = Material.objects.filter(
#         material_name__icontains=query
#     ).values('material_name').distinct()[:10]
    
#     # Return just the names as strings
#     names = [material['material_name'] for material in materials]
#     return JsonResponse(names, safe=False)
    
@login_required
def material(request):
    materials = Material.objects.select_related('model', 'brand').all()
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
def addmaterial(request):
    print(f"🔍 ADD MATERIAL VIEW - Method: {request.method}")
    
    material_brands = MaterialBrand.objects.all()
    material_models = MaterialModel.objects.all()
    hsn_codes = HSNCode.objects.all()
    
    selected_hsn = request.GET.get('selected_hsn', '')

    if request.method == 'POST':
        print("=" * 50)
        print("🚀 FORM SUBMISSION DEBUG INFO")
        print("=" * 50)
        print("✅ POST data received:", dict(request.POST))

        category = request.POST.get('category')
        material_name = request.POST.get('material_name')
        uom = request.POST.get('uom')
        model_name = request.POST.get('model')
        brand_name = request.POST.get('brand')
        description = request.POST.get('description')
        hsn_code = request.POST.get('hsn_code') or selected_hsn
        active_status = request.POST.get('active_status')

        print("📋 VALIDATION STARTED")
        errors = {}

        if not category or category == "Select Category":
            errors['category'] = 'Category is required'
        if not material_name:
            errors['material_name'] = 'Material name is required'
        if not uom or uom == "Select UOM":
            errors['uom'] = 'UOM is required'
        if not hsn_code:
            errors['hsn_code'] = 'HSN code is required'

        # ❌ REMOVED — category must not be unique!
        # if Material.objects.filter(category=category).exists():
        #     errors['category'] = f'Material with category "{category}" already exists!'

        if not errors:
            try:
                model = MaterialModel.objects.filter(name=model_name).first()
                brand = MaterialBrand.objects.filter(name=brand_name).first()

                active_status_bool = active_status == 'True'

                material = Material(
                    category=category,
                    material_name=material_name,
                    uom=uom,
                    hsn_code=hsn_code,
                    model=model,
                    brand=brand,
                    description=description,
                    active_status=active_status_bool
                )

                material.save()

                messages.success(request, f"Material created successfully! Code: {material.material_code}")
                return redirect('ajserp:material')

            except Exception as e:
                messages.error(request, f"Error creating material: {str(e)}")

        else:
            for field, msg in errors.items():
                messages.error(request, msg)

    return render(request, 'ajserpadmin/addmaterial.html', {
        'material_brands': material_brands,
        'material_models': material_models,
        'hsn_codes': hsn_codes,
        'selected_hsn_code': selected_hsn
    })


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

# @login_required
# def warehouse(request):
#     """Warehouse list view"""
#     warehouses = Warehouse.objects.all()
    
#     # Handle search
#     search_query = request.GET.get('search', '')
#     if search_query:
#         warehouses = warehouses.filter(
#             Q(warehouse_code__icontains=search_query) |
#             Q(warehouse_name__icontains=search_query) |
#             Q(city__icontains=search_query) |
#             Q(state__icontains=search_query)
#         )
    
#     context = {
#         'warehouses': warehouses,
#         'search_query': search_query
#     }
#     return render(request, 'ajserpadmin/warehouse.html', context)

@login_required
def warehouse(request):
    """Warehouse list view with search and pagination"""
    warehouses = Warehouse.objects.all().order_by('warehouse_code')
    
    # Handle search
    search_query = request.GET.get('q', '').strip()
    if search_query:
        warehouses = warehouses.filter(
            Q(warehouse_code__icontains=search_query) |
            Q(warehouse_name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(state__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(email_address__icontains=search_query) |
            Q(state_of_supply__icontains=search_query)
        )
    
    # ========== PAGINATION ==========
    paginator = Paginator(warehouses, 10)  # Show 10 warehouses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'warehouses': page_obj,  # Use paginated object
        'page_obj': page_obj,    # For pagination controls
        'search_query': search_query
    }

    return render(request, 'ajserpadmin/warehouse.html', context)

@login_required
def warehouse_global_suggestions(request):
    query = request.GET.get('q', '').strip()
    print(f"🔍 WAREHOUSE GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    suggestions = []
    
    # Search across all warehouse fields
    warehouses = Warehouse.objects.filter(
        Q(warehouse_code__icontains=query) |
        Q(warehouse_name__icontains=query) |
        Q(city__icontains=query) |
        Q(state_of_supply__icontains=query) |
        Q(contact_number__icontains=query) |
        Q(email_address__icontains=query)
    )[:10]  # Limit to 10 results
    
    for warehouse in warehouses:
        if query.lower() in warehouse.warehouse_code.lower():
            suggestions.append({
                'value': warehouse.warehouse_code,
                'text': f"{warehouse.warehouse_code} - {warehouse.warehouse_name}",
                'type': 'Warehouse Code'
            })

        if query.lower() in warehouse.warehouse_name.lower():
            suggestions.append({
                'value': warehouse.warehouse_name,
                'text': f"{warehouse.warehouse_name} ({warehouse.warehouse_code})",
                'type': 'Warehouse Name'
            })

        if query.lower() in warehouse.city.lower():
            suggestions.append({
                'value': warehouse.city,
                'text': f"{warehouse.city} - {warehouse.warehouse_name}",
                'type': 'City'
            })

        if query.lower() in warehouse.state_of_supply.lower():
            suggestions.append({
                'value': warehouse.state_of_supply,
                'text': f"{warehouse.state_of_supply} - {warehouse.warehouse_name}",
                'type': 'State'
            })
    
    # Remove duplicates
    seen = set()
    unique_suggestions = []
    for s in suggestions:
        if s['value'] not in seen:
            seen.add(s['value'])
            unique_suggestions.append(s)
    
    print(f"✅ Found {len(unique_suggestions)} unique suggestions")

    return JsonResponse(unique_suggestions, safe=False)


@login_required
def addwarehouse(request):
    """Add new warehouse"""
    if request.method == 'POST':
        print("🔧 WAREHOUSE FORM SUBMISSION DEBUG")
        print("📝 POST data received:", dict(request.POST))
        
        # Get form data (NO warehouse_code - it will be auto-generated)
        warehouse_name = request.POST.get('warehouse_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        email_address = request.POST.get('email_address', '').strip()
        state_of_supply = request.POST.get('state_of_supply', '').strip()
        gst_number = request.POST.get('gst_number', '').strip()
        address1 = request.POST.get('address1', '').strip()
        description = request.POST.get('description', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        country = request.POST.get('country', 'India').strip()
        postal_code = request.POST.get('postal_code', '').strip()

        print(f"📋 Form Data:")
        print(f"  - Warehouse Name: {warehouse_name}")
        print(f"  - Contact: {contact_number}")
        print(f"  - Email: {email_address}")
        print(f"  - State of Supply: {state_of_supply}")
        print(f"  - GST: {gst_number}")
        print(f"  - Address: {address1}")
        print(f"  - City: {city}")
        print(f"  - State: {state}")
        print(f"  - Postal Code: {postal_code}")

        # Validation (NO warehouse_code validation)
        errors = {}
        if not warehouse_name:
            errors['warehouse_name'] = 'Warehouse name is required'
            print("❌ Warehouse name validation failed")
        
        if not contact_number:
            errors['contact_number'] = 'Contact number is required'
            print("❌ Contact number validation failed")
        
        if not email_address:
            errors['email_address'] = 'Email address is required'
            print("❌ Email address validation failed")
        
        if not state_of_supply:
            errors['state_of_supply'] = 'State of supply is required'
            print("❌ State of supply validation failed")
        
        if not address1:
            errors['address1'] = 'Address is required'
            print("❌ Address validation failed")
        
        if not city:
            errors['city'] = 'City is required'
            print("❌ City validation failed")
        
        if not state or state == "Select State":
            errors['state'] = 'State is required'
            print("❌ State validation failed")
        
        if not country or country == "Select Country":
            errors['country'] = 'Country is required'
            print("❌ Country validation failed")
        
        if not postal_code:
            errors['postal_code'] = 'Postal code is required'
            print("❌ Postal code validation failed")

        if errors:
            print(f"🚨 Validation errors: {errors}")
            for field, error in errors.items():
                messages.error(request, f"{field}: {error}")
            return render(request, 'ajserpadmin/addwarehouse.html', {
                'form_data': request.POST
            })

        try:
            # Create warehouse (warehouse_code will be auto-generated in save() method)
            warehouse = Warehouse(
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
            print(f"✅ Warehouse saved successfully: {warehouse.warehouse_code} - {warehouse.warehouse_name}")

            messages.success(request, f'Warehouse "{warehouse_name}" created successfully! Code: {warehouse.warehouse_code}')
            return redirect('ajserp:warehouse')

        except Exception as e:
            print(f"💥 Error saving warehouse: {str(e)}")
            messages.error(request, f'Error creating warehouse: {str(e)}')
            return render(request, 'ajserpadmin/addwarehouse.html', {
                'form_data': request.POST
            })
    
    # GET request - show empty form
    print("📄 Loading empty warehouse form")
    return render(request, 'ajserpadmin/addwarehouse.html')


@login_required
def edit_warehouse(request, warehouse_code):
    """Edit existing warehouse"""
    try:
        warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
        
        if request.method == 'POST':
            print(f"🔧 EDIT WAREHOUSE FORM - {warehouse_code}")
            
            # Get form data
            warehouse_name = request.POST.get('warehouse_name', '').strip()
            contact_number = request.POST.get('contact_number', '').strip()
            email_address = request.POST.get('email_address', '').strip()
            state_of_supply = request.POST.get('state_of_supply', '').strip()
            gst_number = request.POST.get('gst_number', '').strip()
            address1 = request.POST.get('address1', '').strip()
            description = request.POST.get('description', '').strip()
            city = request.POST.get('city', '').strip()
            state = request.POST.get('state', '').strip()
            country = request.POST.get('country', 'India').strip()
            postal_code = request.POST.get('postal_code', '').strip()

            # Validation
            errors = {}
            if not warehouse_name:
                errors['warehouse_name'] = 'Warehouse name is required'
            if not contact_number:
                errors['contact_number'] = 'Contact number is required'

            if errors:
                for field, error in errors.items():
                    messages.error(request, f"{field}: {error}")
                return render(request, 'ajserpadmin/edit_warehouse.html', {
                    'warehouse': warehouse
                })

            # Update warehouse
            warehouse.warehouse_name = warehouse_name
            warehouse.contact_number = contact_number
            warehouse.email_address = email_address
            warehouse.state_of_supply = state_of_supply
            warehouse.gst_number = gst_number
            warehouse.address1 = address1
            warehouse.description = description
            warehouse.city = city
            warehouse.state = state
            warehouse.country = country
            warehouse.postal_code = postal_code
            warehouse.save()

            messages.success(request, f'Warehouse "{warehouse_name}" updated successfully!')
            return redirect('ajserp:warehouse')

        # GET request - show form with data
        return render(request, 'ajserpadmin/edit_warehouse.html', {
            'warehouse': warehouse
        })
        
    except Warehouse.DoesNotExist:
        messages.error(request, 'Warehouse not found!')
        return redirect('ajserp:warehouse')

@login_required
def delete_warehouse(request, warehouse_code):
    """Delete warehouse"""
    if request.method == 'POST':
        try:
            warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
            warehouse_name = warehouse.warehouse_name
            warehouse.delete()
            messages.success(request, f'Warehouse "{warehouse_name}" deleted successfully!')
        except Warehouse.DoesNotExist:
            messages.error(request, 'Warehouse not found!')
        except Exception as e:
            messages.error(request, f'Error deleting warehouse: {str(e)}')
    
    return redirect('ajserp:warehouse')

# Customer List View
@login_required
def customers(request):
    customers = Customer.objects.select_related('customer_group', 'category').all()
    return render(request, 'ajserpadmin/customers.html', {'customers': customers})

@login_required
def addcustomers(request):
    customer_groups = CustomerGroup.objects.all()
    customer_categories = CustomerCategory.objects.all()
    
    if request.method == 'POST':
        print("🔧 CUSTOMER FORM SUBMISSION DEBUG")
        print("📝 POST data received:", dict(request.POST))
        
        # Direct form handling (NO customer_code - it will be auto-generated)
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
            print("❌ Customer name validation failed")
        if not contact_person:
            errors['contact_person'] = 'Contact person is required'
            print("❌ Contact person validation failed")
        
        if not errors:
            try:
                # Get foreign key objects
                customer_group = CustomerGroup.objects.get(code=customer_group_code) if customer_group_code else None
                category = CustomerCategory.objects.get(code=category_code) if category_code else None
                
                # Create customer (customer_code will be auto-generated in save() method)
                customer = Customer(
                    customer_name=customer_name,
                    contact_person=contact_person,
                    contact_number=contact_number,
                    email_address=email_address,
                    customer_group=customer_group,
                    category=category,
                    gst_number=request.POST.get('gst_number', ''),
                    pan_no=request.POST.get('pan_no', ''),
                    credit_period=request.POST.get('credit_period') or 0,
                    credit_limit=request.POST.get('credit_limit') or 0.00,
                    state_of_supply=request.POST.get('state_of_supply', ''),
                    billing_address1=request.POST.get('billing_address1', ''),
                    billing_address2=request.POST.get('billing_address2', ''),
                    billing_city=request.POST.get('billing_city', ''),
                    billing_state=request.POST.get('billing_state', ''),
                    billing_country=request.POST.get('billing_country', 'India'),
                    billing_postal_code=request.POST.get('billing_postal_code', ''),
                    shipping_address1=request.POST.get('shipping_address1', ''),
                    shipping_address2=request.POST.get('shipping_address2', ''),
                    shipping_city=request.POST.get('shipping_city', ''),
                    shipping_state=request.POST.get('shipping_state', ''),
                    shipping_country=request.POST.get('shipping_country', 'India'),
                    shipping_postal_code=request.POST.get('shipping_postal_code', ''),
                    same_as_billing=same_as_billing
                )
                
                # Handle same_as_billing logic
                if same_as_billing:
                    customer.shipping_address1 = request.POST.get('billing_address1', '')
                    customer.shipping_address2 = request.POST.get('billing_address2', '')
                    customer.shipping_city = request.POST.get('billing_city', '')
                    customer.shipping_state = request.POST.get('billing_state', '')
                    customer.shipping_country = request.POST.get('billing_country', 'India')
                    customer.shipping_postal_code = request.POST.get('billing_postal_code', '')
                
                # Handle image upload
                if 'image' in request.FILES:
                    customer.image = request.FILES['image']
                
                customer.save()
                print(f"✅ Customer saved successfully: {customer.customer_code} - {customer.customer_name}")
                
                messages.success(request, f'Customer created successfully! Code: {customer.customer_code}')
                return redirect('ajserp:customers')
                
            except Exception as e:
                print(f"💥 Error creating customer: {str(e)}")
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
# @login_required
# def materialinward(request):
#     material_inwards = MaterialInward.objects.select_related('vendor', 'model', 'brand', 'hsn_code').all()
#     vendors = Supplier.objects.all()  # ADD THIS LINE
#     return render(request, "ajserpadmin/materialinward.html", {
#         'material_inwards': material_inwards,
#         'vendors': vendors  # ADD THIS LINE
#     })

@login_required
def materialinward(request):
    """
    Combined list view + create form + advanced search + suggestions + pagination
    """

    # ==========================================
    # BASE QUERYSET
    # ==========================================
    material_inwards = MaterialInward.objects.select_related(
        'vendor', 'hsn_code', 'model', 'brand'
    ).all().order_by('-grn_date', '-created_at')

    # From your original code
    vendors = Supplier.objects.all()

    # ==========================================
    # SEARCH & FILTERS
    # ==========================================
    if request.method == 'GET':

        # Global search
        search_query = request.GET.get('q', '')
        if search_query:
            material_inwards = material_inwards.filter(
                Q(grn_number__icontains=search_query) |
                Q(batch__icontains=search_query) |
                Q(invoice_number__icontains=search_query) |
                Q(material_name__icontains=search_query) |
                Q(vendor_name__icontains=search_query)
            )

        # GRN Number filter
        grn_number = request.GET.get('grn_number')
        if grn_number:
            material_inwards = material_inwards.filter(grn_number__icontains=grn_number)

        # Batch filter
        batch = request.GET.get('batch')
        if batch:
            material_inwards = material_inwards.filter(batch__icontains=batch)

        # Vendor filter
        vendor = request.GET.get('vendor')
        if vendor:
            material_inwards = material_inwards.filter(vendor__vendor_code=vendor)

        # Material name filter
        material_name = request.GET.get('material_name')
        if material_name:
            material_inwards = material_inwards.filter(material_name__icontains=material_name)

        # Date range filters
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date:
            material_inwards = material_inwards.filter(grn_date__gte=from_date)
        if to_date:
            material_inwards = material_inwards.filter(grn_date__lte=to_date)

    # ==========================================
    # PAGINATION (10 per page)
    # ==========================================
    paginator = Paginator(material_inwards, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ==========================================
    # CREATE FUNCTIONALITY
    # ==========================================
    if request.method == 'POST':
        try:
            grn_date = request.POST.get('grn_date')
            invoice_date = request.POST.get('invoice_date')
            invoice_number = request.POST.get('invoice_number')
            quantity = request.POST.get('quantity')
            material_code = request.POST.get('material_code')
            vendor_code = request.POST.get('vendor')
            model_name = request.POST.get('model')
            brand_name = request.POST.get('brand')

            # Required validation
            if not all([grn_date, invoice_date, invoice_number, quantity, material_code, vendor_code]):
                messages.error(request, "Please fill all required fields.")
                return redirect('ajserp:materialinward')

            # Material
            try:
                material = Material.objects.get(material_code=material_code)
            except Material.DoesNotExist:
                messages.error(request, "Material not found.")
                return redirect('ajserp:materialinward')

            # Vendor
            try:
                vendor = Supplier.objects.get(vendor_code=vendor_code)
            except Supplier.DoesNotExist:
                messages.error(request, "Vendor not found.")
                return redirect('ajserp:materialinward')

            # HSN code
            try:
                hsn_code = HSNCode.objects.get(hsn_code=material.hsn_code)
            except HSNCode.DoesNotExist:
                messages.error(request, "HSN code not found.")
                return redirect('ajserp:materialinward')

            # Optional model
            model = MaterialModel.objects.filter(name=model_name).first() if model_name else None

            # Optional brand
            brand = MaterialBrand.objects.filter(name=brand_name).first() if brand_name else None

            # Create entry
            inward = MaterialInward(
                grn_date=grn_date,
                invoice_date=invoice_date,
                invoice_number=invoice_number,
                quantity=quantity,
                material_code=material.material_code,
                material_name=material.material_name,
                uom=material.uom,
                category=material.category,
                vendor=vendor,
                vendor_name=vendor.vendor_name,
                hsn_code=hsn_code,
                model=model,
                brand=brand
            )

            inward.full_clean()
            inward.save()

            messages.success(request, f"Material inward {inward.grn_number} created successfully!")
            return redirect('ajserp:materialinward')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    # ==========================================
    # CONTEXT FOR TEMPLATE
    # ==========================================
    context = {
        'material_inwards': page_obj,
        'page_obj': page_obj,
        'vendors': vendors,
        'suppliers': Supplier.objects.all(),
        'materials': Material.objects.all(),
        'hsn_codes': HSNCode.objects.all(),
        'material_models': MaterialModel.objects.all(),
        'material_brands': MaterialBrand.objects.all(),
        'search_params': request.GET,
        'today': timezone.now().date().isoformat(),
    }

    return render(request, "ajserpadmin/materialinward.html", context)

@login_required
def grn_number_suggestions(request):
    """API for GRN number search suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 GRN SUGGESTIONS - Query: '{query}'")

    if len(query) < 2:
        print("❌ Query too short")
        return JsonResponse([], safe=False)
    
    # Search in MaterialInward model for GRN numbers
    grn_numbers = MaterialInward.objects.filter(
        grn_number__icontains=query
    ).values_list('grn_number', flat=True).distinct()[:10]
    
    # TEMPORARY: If no data, return test data
    if not grn_numbers:
        print("⚠ No GRN data found, returning test data")
        test_data = ['GRN001', 'GRN002', 'GRN003', 'GRN004', 'GRN005']
        filtered = [grn for grn in test_data if query.upper() in grn]
        print(f"✅ Test GRN data: {filtered}")
        return JsonResponse(filtered, safe=False)

    print(f"✅ Found GRN numbers: {list(grn_numbers)}")

    # Return just the GRN numbers as strings
    numbers = list(grn_numbers)
    return JsonResponse(numbers, safe=False)

@login_required
def batch_suggestions(request):
    """API for Batch search suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 BATCH SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        print("❌ Query too short")
        return JsonResponse([], safe=False)
    
    # Search in MaterialInward model for Batch numbers
    batches = MaterialInward.objects.filter(
        batch__icontains=query
    ).values_list('batch', flat=True).distinct()[:10]

    # TEMPORARY: If no data, return test data
    if not batches:
        print("⚠ No batch data found, returning test data")
        test_data = ['BATCH001', 'BATCH002', 'BATCH003', 'BATCH004', 'BATCH005']
        filtered = [batch for batch in test_data if query.upper() in batch]
        print(f"✅ Test batch data: {filtered}")
        return JsonResponse(filtered, safe=False)
    
    print(f"✅ Found batches: {list(batches)}")

    # Return just the batch numbers as strings
    batch_list = list(batches)
    return JsonResponse(batch_list, safe=False)


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
    """API for vendor autocomplete with address fields"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in both vendor_code and vendor_name
    vendors = Supplier.objects.filter(
        Q(vendor_code__icontains=query) | 
        Q(vendor_name__icontains=query)
    ).values(
        'vendor_code', 
        'vendor_name',
        'billing_address1',
        'billing_address2', 
        'billing_city',
        'billing_state',
        'billing_postal_code',
        'shipping_address1',
        'shipping_address2',
        'shipping_city',
        'shipping_state',
        'shipping_postal_code',
        'same_as_billing'
    )[:10]
    
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


@login_required
def addpricelists(request):
    materials = Material.objects.select_related('model', 'brand').all()
    
    # Handle price updates
    if request.method == 'POST':
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
                pricing_status = statuses[i] if i < len(statuses) else 'Active'
                
                # Validation
                if selling_price and mrp_price and float(selling_price) > float(mrp_price):
                    messages.warning(request, f"Selling price cannot be greater than MRP for {material_code}")
                    continue
                
                # Update Material fields directly
                material.mrp = mrp_price
                material.selling_price = selling_price
                material.price_from_date = from_date
                material.price_to_date = to_date
                material.pricing_status = pricing_status
                material.save()
                
                updated_count += 1
                
            except Exception as e:
                messages.error(request, f"Error updating {material_code}: {str(e)}")
        
        if updated_count > 0:
            messages.success(request, f"Updated {updated_count} materials")
        
        return redirect('ajserp:addpricelists')
    
    context = {
        'materials': materials,
    }
    
    return render(request, 'ajserpadmin/addpricelists.html', context)

@login_required
def edit_price(request, material_code):
    print(f"🔍 EDIT PRICE VIEW CALLED - Material Code: {material_code}")
    print(f"🔍 Request Method: {request.method}")
    
    try:
        material = Material.objects.get(material_code=material_code)
        print(f"✅ Material found: {material.material_name}")
        
        if request.method == 'POST':
            print("📝 POST data received:", dict(request.POST))
            mrp_price = request.POST.get('mrp_price')
            selling_price = request.POST.get('selling_price')
            
            print(f"📊 MRP: {mrp_price}, Selling Price: {selling_price}")
            
            errors = {}
            if not mrp_price:
                errors['mrp_price'] = 'MRP is required'
            if not selling_price:
                errors['selling_price'] = 'Selling price is required'
            
            # Validation - Selling price cannot be greater than MRP
            if selling_price and mrp_price and float(selling_price) > float(mrp_price):
                errors['selling_price'] = 'Selling price cannot be greater than MRP'
            
            if not errors:
                material.mrp = mrp_price
                material.selling_price = selling_price
                material.save()
                
                print(f"✅ Price updated: MRP={mrp_price}, Selling={selling_price}")
                messages.success(request, f'Price updated successfully for {material.material_name}!')
                return redirect('ajserp:addpricelists')
            else:
                for error in errors.values():
                    messages.error(request, error)
        
        return render(request, 'ajserpadmin/addpricelists.html', {
            'material': material,
        })
    
    except Material.DoesNotExist:
        print(f"❌ Material not found: {material_code}")
        messages.error(request, 'Material not found!')
        return redirect('ajserp:addpricelists')
@login_required
def delete_price(request, material_code):
    if request.method == 'POST':
        try:
            material = Material.objects.get(material_code=material_code)
            material_name = material.material_name
            
            # Reset price fields to default/zero
            material.mrp = 0
            material.selling_price = 0
            material.price_from_date = None
            material.price_to_date = None
            material.pricing_status = 'Inactive'
            material.save()
            
            messages.success(request, f'Prices reset for {material_name} successfully!')
        except Material.DoesNotExist:
            messages.error(request, 'Material not found!')
        except Exception as e:
            messages.error(request, f'Error resetting prices: {str(e)}')
    
    return redirect('ajserp:addpricelists')

@login_required
def addestimate(request):
    if request.method == 'POST':
        try:
            # Create Estimate
            estimate = Estimate.objects.create(
                customer_id=request.POST.get('customer'),
                warehouse_id=request.POST.get('warehouse'),
                created_by=request.user,
                billing_address1=request.POST.get('billing_address1', ''),
                billing_city=request.POST.get('billing_city', ''),
                billing_state=request.POST.get('billing_state', ''),
                billing_postal_code=request.POST.get('billing_postal_code', ''),
                round_off=request.POST.get('round_off', 0),
                description=request.POST.get('description', ''),
                terms_conditions=request.POST.get('terms_conditions', '')
            )
            
            # Create Estimate Items
            items_data = {}
            for key, value in request.POST.items():
                if key.startswith('items['):
                    # Parse the field name: items[1][quantity] -> index=1, field=quantity
                    parts = key.split('[')
                    if len(parts) >= 3:
                        index = parts[1].replace(']', '')
                        field = parts[2].replace(']', '')
                        
                        if index not in items_data:
                            items_data[index] = {}
                        items_data[index][field] = value
            
            # Create estimate items
            for index, item_data in items_data.items():
                EstimateItem.objects.create(
                    estimate=estimate,
                    material_id=item_data.get('material'),
                    material_name=item_data.get('material_name'),
                    quantity=item_data.get('quantity', 1),
                    mrp=item_data.get('mrp', 0),
                    discount=item_data.get('discount', 0),
                    cgst_rate=item_data.get('cgst_rate', 0),
                    sgst_rate=item_data.get('sgst_rate', 0),
                    igst_rate=item_data.get('igst_rate', 0),
                    cess_rate=item_data.get('cess_rate', 0),
                    sequence=int(index)
                )
            
            # Calculate totals
            estimate.calculate_totals()
            
        #     return redirect('estimate_detail', estimate_id=estimate.id)
            
        # except Exception as e:
        #     # Handle error
        #     pass
            messages.success(request, f'Estimate created successfully! ID: {estimate.id}')
            return redirect('ajserp:estimate')  # Redirect to estimate list
            
        except Exception as e:
            print(f"Error creating estimate: {str(e)}")
            messages.error(request, f'Error creating estimate: {str(e)}')
    # GET request - show form
    materials = Material.objects.all()
    customers = Customer.objects.all()
    warehouses = Warehouse.objects.all()
    
    context = {
        'materials': materials,
        'customers': customers,
        'warehouses': warehouses,
    }
    return render(request, 'ajserpadmin/addestimate.html', context)

@login_required
# API Views
def materialestimate_autocomplete(request):
    query = request.GET.get('q', '').strip()
    print(f"🔍 Material Autocomplete Query: '{query}'")  # Debug
    
    if len(query) < 1:  # Changed from 2 to 1 for better search
        return JsonResponse([], safe=False)
    
    try:
        # Search in multiple fields with better filtering
        materials = Material.objects.filter(
            Q(material_name__icontains=query) | 
            Q(material_code__icontains=query) |
            Q(hsn_code__icontains=query)
        ).select_related('model', 'brand')[:10]
        
        print(f"✅ Found {materials.count()} materials")  # Debug
        
        data = []
        for material in materials:
            material_data = {
                'material_code': material.material_code,
                'material_name': material.material_name,
                
                'mrp': float(material.mrp),
                'hsn_code': material.hsn_code,
                
            }
            data.append(material_data)
            print(f"📦 Material: {material.material_code} - {material.material_name}")  # Debug
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        print(f"❌ Material Autocomplete Error: {str(e)}")  # Debug
        return JsonResponse([], safe=False)

@login_required
def get_tax_rates(request):
    hsn_code = request.GET.get('hsn_code', '')
    print(f"📊 DEBUG: Getting tax rates for HSN: {hsn_code}")  # Debug log
    
    try:
        # First get the HSNCode object, then find the tax rates
        hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
        tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
        
        data = {
            'cgst': float(tax_rate.cgst),
            'sgst': float(tax_rate.sgst),
            'igst': float(tax_rate.igst),
            'cess': float(tax_rate.cess),
            'success': True
        }
        print(f"✅ DEBUG: Tax rates found: {data}")  # Debug log
        
    except HSNCode.DoesNotExist:
        print(f"❌ DEBUG: HSN Code not found: {hsn_code}")  # Debug log
        data = {
            'cgst': 0,
            'sgst': 0,
            'igst': 0,
            'cess': 0,
            'success': False,
            'message': 'HSN code not found'
        }
    except Taxes.DoesNotExist:
        print(f"❌ DEBUG: Tax rates not found for HSN: {hsn_code}")  # Debug log
        data = {
            'cgst': 0,
            'sgst': 0,
            'igst': 0,
            'cess': 0,
            'success': False,
            'message': 'Tax rates not found for this HSN code'
        }
    except Exception as e:
        print(f"❌ DEBUG: Error getting tax rates: {str(e)}")  # Debug log
        data = {
            'cgst': 0,
            'sgst': 0,
            'igst': 0,
            'cess': 0,
            'success': False,
            'message': f'Error: {str(e)}'
        }
    
    return JsonResponse(data)

@login_required
def get_customer_address(request):
    customer_code = request.GET.get('customer_code', '')
    try:
        customer = Customer.objects.get(customer_code=customer_code)
        data = {
            'billing_address1': customer.billing_address1,
            'billing_address2': customer.billing_address2 or '',
            'billing_city': customer.billing_city,
            'billing_state': customer.billing_state,
            'billing_postal_code': customer.billing_postal_code,
            'success': True
        }
    except Customer.DoesNotExist:
        data = {
            'success': False,
            'message': 'Customer not found'
        }
    
    return JsonResponse(data)

@login_required
# Customer Autocomplete API
def customer_autocomplete(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in customer name and code
    customers = Customer.objects.filter(
        Q(customer_name__icontains=query) | 
        Q(customer_code__icontains=query)
    ).values('customer_code', 'customer_name', 'billing_address1', 'billing_address2', 
             'billing_city', 'billing_state', 'billing_postal_code')[:10]
    
    customer_list = []
    for customer in customers:
        customer_list.append({
            'customer_code': customer['customer_code'],
            'customer_name': customer['customer_name'],
            'billing_address1': customer['billing_address1'],
            'billing_address2': customer['billing_address2'] or '',
            'billing_city': customer['billing_city'],
            'billing_state': customer['billing_state'],
            'billing_postal_code': customer['billing_postal_code'],
        })
    
    return JsonResponse(customer_list, safe=False)

@login_required
# Warehouse Autocomplete API
def warehouse_autocomplete(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in warehouse name and code
    warehouses = Warehouse.objects.filter(
        Q(warehouse_name__icontains=query) | 
        Q(warehouse_code__icontains=query)
    ).values('warehouse_code', 'warehouse_name')[:10]
    
    warehouse_list = []
    for warehouse in warehouses:
        warehouse_list.append({
            'warehouse_code': warehouse['warehouse_code'],
            'warehouse_name': warehouse['warehouse_name'],
        })
    
    return JsonResponse(warehouse_list, safe=False)

@login_required
# Get Customer Details API (for auto-filling billing address)
def get_customer_details(request):
    customer_code = request.GET.get('customer_code', '')
    try:
        customer = Customer.objects.get(customer_code=customer_code)
        data = {
            'customer_code': customer.customer_code,
            'customer_name': customer.customer_name,
            'billing_address1': customer.billing_address1,
            'billing_address2': customer.billing_address2 or '',
            'billing_city': customer.billing_city,
            'billing_state': customer.billing_state,
            'billing_postal_code': customer.billing_postal_code,
            'success': True
        }
    except Customer.DoesNotExist:
        data = {
            'success': False,
            'message': 'Customer not found'
        }
    
    return JsonResponse(data)

# Add these functions to your views.py
def get_estimate_suggestions(request):
    """Get estimate number suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 ESTIMATE SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        estimates = Estimate.objects.filter(
            estimate_number__icontains=query
        ).values('estimate_number', 'customer__customer_name')[:10]
        
        suggestions = []
        for estimate in estimates:
            suggestions.append({
                'value': estimate['estimate_number'],
                'text': f"{estimate['estimate_number']} - {estimate['customer__customer_name']}"
            })
        
        print(f"✅ Found {len(suggestions)} estimate suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_estimate_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

def get_customer_suggestions(request):
    """Get customer name suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 CUSTOMER SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        customers = Customer.objects.filter(
            customer_name__icontains=query
        ).values('customer_name')[:10]
        
        suggestions = [{'value': cust['customer_name'], 'text': cust['customer_name']} for cust in customers]
        print(f"✅ Found {len(suggestions)} customer suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_customer_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

def get_global_suggestions(request):
    """Get global search suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search estimate numbers
        estimates = Estimate.objects.filter(estimate_number__icontains=query)[:5]
        for est in estimates:
            suggestions.append({
                'value': est.estimate_number,
                'text': f"Estimate: {est.estimate_number} - {est.customer.customer_name}"
            })
        
        # Search customer names  
        customers = Customer.objects.filter(customer_name__icontains=query)[:5]
        for cust in customers:
            suggestions.append({
                'value': cust.customer_name,
                'text': f"Customer: {cust.customer_name}"
            })
        
        print(f"✅ Found {len(suggestions)} global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    
@login_required
def edit_estimate(request, estimate_id):
    """Edit an existing estimate"""
    estimate = get_object_or_404(Estimate, id=estimate_id)
    
    if request.method == 'POST':
        try:
            print(f"🔧 EDITING ESTIMATE {estimate.estimate_number}")
            print("📝 POST data:", dict(request.POST))
            
            # Get basic info
            customer_id = request.POST.get('customer')
            date = request.POST.get('date')
            valid_till = request.POST.get('valid_till')
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            # Get customer
            customer = get_object_or_404(Customer, id=customer_id)
            
            # Update estimate fields
            estimate.customer = customer
            estimate.date = date
            estimate.valid_till = valid_till
            estimate.ref_number = ref_number
            estimate.description = description
            estimate.terms_conditions = terms_conditions
            estimate.billing_address1 = billing_address1
            estimate.billing_address2 = billing_address2
            estimate.billing_city = billing_city
            estimate.billing_state = billing_state
            estimate.billing_postal_code = billing_postal_code
            estimate.round_off = round_off
            
            # Handle line items if provided
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            if material_names and material_names[0]:  # If items are provided
                # Delete existing items
                estimate.estimate_items.all().delete()
                
                # Create new items
                for i in range(len(material_names)):
                    if material_names[i]:
                        try:
                            material = Material.objects.get(material_name=material_names[i])
                            
                            quantity = float(quantities[i]) if quantities[i] else 0
                            mrp = float(mrps[i]) if mrps[i] else 0
                            discount = float(discounts[i]) if discounts[i] else 0
                            
                            # Get tax rates
                            try:
                                hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                                tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                                cgst_percent = float(tax_rate.cgst)
                                sgst_percent = float(tax_rate.sgst)
                                igst_percent = float(tax_rate.igst)
                                cess_percent = float(tax_rate.cess)
                            except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                                # Use default tax rates if not found
                                cgst_percent = 9
                                sgst_percent = 9
                                igst_percent = 18
                                cess_percent = 0
                            
                            # Calculate amounts
                            after_discount = mrp - discount
                            basic_amount = quantity * after_discount
                            cgst_amount = (basic_amount * cgst_percent) / 100
                            sgst_amount = (basic_amount * sgst_percent) / 100
                            igst_amount = (basic_amount * igst_percent) / 100
                            cess_amount = (basic_amount * cess_percent) / 100
                            tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                            final_amount = basic_amount + tax_amount
                            
                            # Create estimate item
                            EstimateItem.objects.create(
                                estimate=estimate,
                                material=material,
                                material_name=material_names[i],
                                quantity=quantity,
                                mrp=mrp,
                                discount=discount,
                                amount=round(basic_amount, 2),
                                sgst_rate=sgst_percent,
                                cgst_rate=cgst_percent,
                                igst_rate=igst_percent,
                                cess_rate=cess_percent,
                                sgst_amount=round(sgst_amount, 2),
                                cgst_amount=round(cgst_amount, 2),
                                igst_amount=round(igst_amount, 2),
                                cess_amount=round(cess_amount, 2),
                                sequence=i + 1
                            )
                            
                        except Material.DoesNotExist:
                            messages.error(request, f'Material "{material_names[i]}" not found!')
                            return redirect('ajserp:estimate')
                        except Exception as e:
                            messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                            return redirect('ajserp:estimate')
            
            # Recalculate totals
            estimate.calculate_totals()
            estimate.save()
            
            messages.success(request, f'Estimate {estimate.estimate_number} updated successfully!')
            return redirect('ajserp:estimate')
            
        except Exception as e:
            print(f"❌ Error updating estimate: {str(e)}")
            messages.error(request, f'Error updating estimate: {str(e)}')
            return redirect('ajserp:estimate')
    
    # For GET request, you might want to show an edit form
    # For now, redirect to estimate list
    return redirect('ajserp:estimate')

@login_required
def delete_estimate(request, estimate_id):
    """Delete an estimate"""
    if request.method == 'POST':
        try:
            estimate = get_object_or_404(Estimate, id=estimate_id)
            estimate_number = estimate.estimate_number
            estimate.delete()
            messages.success(request, f'Estimate {estimate_number} deleted successfully!')
        except Estimate.DoesNotExist:
            messages.error(request, 'Estimate not found!')
        except Exception as e:
            messages.error(request, f'Error deleting estimate: {str(e)}')
    
    return redirect('ajserp:estimate')


@login_required
def create_estimate(request):
    
    if request.method == 'GET':
        from datetime import date
        today = date.today().isoformat()
        return render(request, 'ajserpadmin/addestimate.html', {'today': today})
    
    if request.method == 'POST':
        # ============ CALCULATION LOGIC FOR SAVE BUTTON ============
        # Check if it's JSON request (from Save button)
        if request.content_type == 'application/json':
            try:
                print("🔢 CALCULATION REQUEST from Save button")
                data = json.loads(request.body)
                
                line_items = data.get('line_items', [])
                round_off = float(data.get('round_off', 0))
                
                print(f"📦 Calculation data - Items: {len(line_items)}, Round Off: {round_off}")
                
                calculated_items = []
                taxable_total = 0
                cgst_total = 0
                sgst_total = 0
                igst_total = 0
                cess_total = 0
                total_amount = 0
                
                # Perform calculation for each line item
                for i, item in enumerate(line_items):
                    quantity = float(item.get('quantity', 0))
                    mrp = float(item.get('mrp', 0))
                    discount = float(item.get('discount', 0))
                    hsn_code = item.get('hsn_code', '')
                    
                    print(f"🔍 Processing item {i+1}: Qty={quantity}, MRP={mrp}, Discount={discount}, HSN={hsn_code}")
                    
                    # Get tax rates
                    try:
                        hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
                        tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                        cgst_percent = float(tax_rate.cgst)
                        sgst_percent = float(tax_rate.sgst)
                        igst_percent = float(tax_rate.igst)
                        cess_percent = float(tax_rate.cess)
                        print(f"✅ Tax rates found: CGST={cgst_percent}, SGST={sgst_percent}")
                    except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                        # Use default tax rates
                        cgst_percent = 9
                        sgst_percent = 9
                        igst_percent = 18
                        cess_percent = 0
                        print(f"⚠️ Using default tax rates for HSN: {hsn_code}")
                    
                    # Calculate amounts
                    after_discount = mrp - discount
                    basic_amount = quantity * after_discount
                    cgst_amount = (basic_amount * cgst_percent) / 100
                    sgst_amount = (basic_amount * sgst_percent) / 100
                    igst_amount = (basic_amount * igst_percent) / 100
                    cess_amount = (basic_amount * cess_percent) / 100
                    tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                    final_amount = basic_amount + tax_amount
                    
                    # Round to 2 decimal places
                    calculated_items.append({
                        'basic_amount': round(basic_amount, 2),
                        'tax_amount': round(tax_amount, 2),
                        'final_amount': round(final_amount, 2),
                        'cgst_amount': round(cgst_amount, 2),
                        'sgst_amount': round(sgst_amount, 2),
                        'igst_amount': round(igst_amount, 2),
                        'cess_amount': round(cess_amount, 2),
                    })
                    
                    # Update totals
                    taxable_total += basic_amount
                    cgst_total += cgst_amount
                    sgst_total += sgst_amount
                    igst_total += igst_amount
                    cess_total += cess_amount
                    total_amount += final_amount
                
                # Calculate grand total with round off
                grand_total = total_amount + round_off
                
                # Round totals
                totals = {
                    'taxable_amount': round(taxable_total, 2),
                    'cgst_total': round(cgst_total, 2),
                    'sgst_total': round(sgst_total, 2),
                    'igst_total': round(igst_total, 2),
                    'cess_total': round(cess_total, 2),
                    'grand_total': round(grand_total, 2)
                }
                
                print(f"✅ Calculation completed: {totals}")
                
                return JsonResponse({
                    'success': True,
                    'line_items': calculated_items,
                    'totals': totals
                })
                
            except Exception as e:
                print(f"❌ Calculation error: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        
        # ============ FORM SUBMISSION LOGIC FOR CREATE BUTTON ============
        else:
            print("💾 FORM SUBMISSION from Create button")
            
            # YOUR EXISTING FORM SUBMISSION CODE
            print("🔍 DEBUG: Starting create_estimate view")
            print("🔍 DEBUG: POST data:", dict(request.POST))
            
            # Get basic info
            customer_code = request.POST.get('customer_code')
            warehouse_code = request.POST.get('warehouse_code')
            date = request.POST.get('date')
            valid_till = request.POST.get('valid_till')
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            print(f"🔍 DEBUG: Customer Code: {customer_code}")
            print(f"🔍 DEBUG: Warehouse Code: {warehouse_code}")
            
            # Get customer and warehouse objects
            try:
                customer = Customer.objects.get(customer_code=customer_code)
                warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
                print(f"✅ DEBUG: Found customer: {customer.customer_name}")
                print(f"✅ DEBUG: Found warehouse: {warehouse.warehouse_name}")
            except Customer.DoesNotExist:
                messages.error(request, f'Customer with code {customer_code} not found!')
                return redirect('ajserp:addestimate')
            except Warehouse.DoesNotExist:
                messages.error(request, f'Warehouse with code {warehouse_code} not found!')
                return redirect('ajserp:addestimate')
            
            # Get all line items
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            print(f"🔍 DEBUG: Material names: {material_names}")
            print(f"🔍 DEBUG: Quantities: {quantities}")
            print(f"🔍 DEBUG: HSN Codes: {hsn_codes}")
            
            line_items = []
            total_taxable = 0
            total_cgst = 0
            total_sgst = 0
            total_igst = 0
            total_cess = 0
            total_amount = 0
            
            # SERVER-SIDE CALCULATION (EXACTLY like JavaScript)
            for i in range(len(material_names)):
                if material_names[i]:
                    try:
                        # Get values
                        quantity = float(quantities[i]) if quantities[i] else 0
                        mrp = float(mrps[i]) if mrps[i] else 0
                        discount = float(discounts[i]) if discounts[i] else 0
                        
                        print(f"🔍 DEBUG: Processing material {i+1}: {material_names[i]}")
                        print(f"🔍 DEBUG: Qty: {quantity}, MRP: {mrp}, Discount: {discount}")
                        
                        # Get material object
                        material = Material.objects.get(material_name=material_names[i])
                        
                        # Get tax rates from database - NO FALLBACK, ERROR IF NOT FOUND
                        try:
                            hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                            tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                            cgst_percent = float(tax_rate.cgst)
                            sgst_percent = float(tax_rate.sgst)
                            igst_percent = float(tax_rate.igst)
                            cess_percent = float(tax_rate.cess)
                            print(f"✅ DEBUG: Found tax rates - CGST: {cgst_percent}, SGST: {sgst_percent}, IGST: {igst_percent}, Cess: {cess_percent}")
                        except (HSNCode.DoesNotExist, Taxes.DoesNotExist) as e:
                            messages.error(request, f'Tax rates not found for HSN code: {hsn_codes[i]}')
                            return redirect('ajserp:addestimate')
                        
                        # EXACT JAVASCRIPT CALCULATION LOGIC
                        # After_Discount = MRP - Discount
                        # Line_basic = Quantity × After_Discount
                        # Line_CGST_Amt = Line_basic x CGST / 100
                        # Line_SGST_Amt = Line_basic x SGST / 100
                        # Line_IGST_Amt = Line_basic x IGST / 100
                        # Line_Cess_Amt = Line_basic x Cess / 100
                        # Line_Tax = Line_CGST_Amt + Line_SGST_Amt + Line_IGST_Amt + Line_Cess_Amt
                        # Line_Amount = Line_basic + Line_Tax
                        
                        # Step 1: After Discount
                        after_discount = mrp - discount
                        
                        # Step 2: Line Basic Amount (Taxable Amount)
                        basic_amount = quantity * after_discount
                        
                        # Step 3: Calculate individual tax amounts
                        cgst_amount = (basic_amount * cgst_percent) / 100
                        sgst_amount = (basic_amount * sgst_percent) / 100
                        igst_amount = (basic_amount * igst_percent) / 100
                        cess_amount = (basic_amount * cess_percent) / 100
                        
                        # Step 4: Total Tax Amount
                        tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                        
                        # Step 5: Final Line Amount
                        final_amount = basic_amount + tax_amount
                        
                        # ROUNDING (Same as JavaScript - to 2 decimal places)
                        basic_amount = round(basic_amount, 2)
                        cgst_amount = round(cgst_amount, 2)
                        sgst_amount = round(sgst_amount, 2)
                        igst_amount = round(igst_amount, 2)
                        cess_amount = round(cess_amount, 2)
                        tax_amount = round(tax_amount, 2)
                        final_amount = round(final_amount, 2)
                        
                        print(f"📊 DEBUG: Calculation Results:")
                        print(f"📊 DEBUG: After Discount: {after_discount}")
                        print(f"📊 DEBUG: Basic Amount: {basic_amount}")
                        print(f"📊 DEBUG: CGST Amount: {cgst_amount} ({cgst_percent}%)")
                        print(f"📊 DEBUG: SGST Amount: {sgst_amount} ({sgst_percent}%)")
                        print(f"📊 DEBUG: IGST Amount: {igst_amount} ({igst_percent}%)")
                        print(f"📊 DEBUG: Cess Amount: {cess_amount} ({cess_percent}%)")
                        print(f"📊 DEBUG: Tax Amount: {tax_amount}")
                        print(f"📊 DEBUG: Final Amount: {final_amount}")
                        
                        # Store line item data
                        line_items.append({
                            'material': material,
                            'material_name': material_names[i],
                            'quantity': quantity,
                            'mrp': mrp,
                            'discount': discount,
                            'basic_amount': basic_amount,
                            'cgst_amount': cgst_amount,
                            'sgst_amount': sgst_amount,
                            'igst_amount': igst_amount,
                            'cess_amount': cess_amount,
                            'tax_amount': tax_amount,
                            'final_amount': final_amount,
                            'cgst_rate': cgst_percent,
                            'sgst_rate': sgst_percent,
                            'igst_rate': igst_percent,
                            'cess_rate': cess_percent,
                        })
                        
                        # Update totals
                        total_taxable += basic_amount
                        total_cgst += cgst_amount
                        total_sgst += sgst_amount
                        total_igst += igst_amount
                        total_cess += cess_amount
                        total_amount += final_amount
                        
                    except Material.DoesNotExist:
                        messages.error(request, f'Material "{material_names[i]}" not found!')
                        return redirect('ajserp:addestimate')
                    except Exception as e:
                        messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                        return redirect('ajserp:addestimate')
            
            # Calculate grand total with round off
            grand_total = total_amount + round_off
            
            # Round totals to 2 decimal places (same as JavaScript)
            total_taxable = round(total_taxable, 2)
            total_cgst = round(total_cgst, 2)
            total_sgst = round(total_sgst, 2)
            total_igst = round(total_igst, 2)
            total_cess = round(total_cess, 2)
            total_amount = round(total_amount, 2)
            grand_total = round(grand_total, 2)
            
            print(f"🎯 DEBUG: Final Totals:")
            print(f"🎯 DEBUG: Taxable Amount: {total_taxable}")
            print(f"🎯 DEBUG: CGST Total: {total_cgst}")
            print(f"🎯 DEBUG: SGST Total: {total_sgst}")
            print(f"🎯 DEBUG: IGST Total: {total_igst}")
            print(f"🎯 DEBUG: Cess Total: {total_cess}")
            print(f"🎯 DEBUG: Total Amount: {total_amount}")
            print(f"🎯 DEBUG: Round Off: {round_off}")
            print(f"🎯 DEBUG: Grand Total: {grand_total}")
            
            # Create Estimate
            estimate = Estimate.objects.create(
                customer=customer,
                warehouse=warehouse,
                date=date,
                valid_till=valid_till,
                ref_number=ref_number,
                description=description,
                terms_conditions=terms_conditions,
                billing_address1=billing_address1,
                billing_address2=billing_address2,
                billing_city=billing_city,
                billing_state=billing_state,
                billing_postal_code=billing_postal_code,
                taxable_amount=total_taxable,
                cgst=total_cgst,
                sgst=total_sgst,
                igst=total_igst,
                cess=total_cess,
                round_off=round_off,
                grand_total=grand_total,
                created_by=request.user
            )
            
            # Create Estimate Items
            for i, item_data in enumerate(line_items):
                EstimateItem.objects.create(
                    estimate=estimate,
                    material=item_data['material'],
                    material_name=item_data['material_name'],
                    quantity=item_data['quantity'],
                    mrp=item_data['mrp'],
                    discount=item_data['discount'],
                    amount=item_data['basic_amount'],  # This is the basic amount (taxable)
                    sgst_rate=item_data['sgst_rate'],
                    cgst_rate=item_data['cgst_rate'],
                    igst_rate=item_data['igst_rate'],
                    cess_rate=item_data['cess_rate'],
                    sgst_amount=item_data['sgst_amount'],
                    cgst_amount=item_data['cgst_amount'],
                    igst_amount=item_data['igst_amount'],
                    cess_amount=item_data['cess_amount'],
                    sequence=i + 1
                )
            
            messages.success(request, f'Estimate created successfully! Estimate Number: {estimate.estimate_number}')
            return redirect('ajserp:estimate')
    
    # # If GET request, show the form
    # return render(request, 'ajserpadmin/addestimate.html')
    
@login_required
def addsalesorders(request):
    if request.method == 'POST':
        try:
            # Create Sales Order
            sales_order = SalesOrder.objects.create(
                customer_id=request.POST.get('customer'),
                warehouse_id=request.POST.get('warehouse'),
                created_by=request.user,
                billing_address1=request.POST.get('billing_address1', ''),
                billing_city=request.POST.get('billing_city', ''),
                billing_state=request.POST.get('billing_state', ''),
                billing_postal_code=request.POST.get('billing_postal_code', ''),
                round_off=request.POST.get('round_off', 0),
                description=request.POST.get('description', ''),
                terms_conditions=request.POST.get('terms_conditions', ''),
                delivery_date=request.POST.get('delivery_date', ''),
                payment_terms=request.POST.get('payment_terms', ''),
                delivery_terms=request.POST.get('delivery_terms', '')
            )
            
            # Create Sales Order Items
            items_data = {}
            for key, value in request.POST.items():
                if key.startswith('items['):
                    # Parse the field name: items[1][quantity] -> index=1, field=quantity
                    parts = key.split('[')
                    if len(parts) >= 3:
                        index = parts[1].replace(']', '')
                        field = parts[2].replace(']', '')
                        
                        if index not in items_data:
                            items_data[index] = {}
                        items_data[index][field] = value
            
            # Create sales order items
            for index, item_data in items_data.items():
                SalesOrderItem.objects.create(
                    sales_order=sales_order,
                    material_id=item_data.get('material'),
                    material_name=item_data.get('material_name'),
                    quantity=item_data.get('quantity', 1),
                    mrp=item_data.get('mrp', 0),
                    discount=item_data.get('discount', 0),
                    cgst_rate=item_data.get('cgst_rate', 0),
                    sgst_rate=item_data.get('sgst_rate', 0),
                    igst_rate=item_data.get('igst_rate', 0),
                    cess_rate=item_data.get('cess_rate', 0),
                    sequence=int(index)
                )
            
            # Calculate totals
            sales_order.calculate_totals()
            
            messages.success(request, f'Sales Order created successfully! Order Number: {sales_order.order_number}')
            return redirect('ajserp:salesorders')
            
        except Exception as e:
            print(f"Error creating sales order: {str(e)}")
            messages.error(request, f'Error creating sales order: {str(e)}')
    
    # GET request - show form
    materials = Material.objects.all()
    customers = Customer.objects.all()
    warehouses = Warehouse.objects.all()
    
    context = {
        'materials': materials,
        'customers': customers,
        'warehouses': warehouses,
    }
    return render(request, 'ajserpadmin/addsalesorders.html', context)

@login_required
def create_sales_order(request):
    
    if request.method == 'GET':
        from datetime import date
        today = date.today().isoformat()
        return render(request, 'ajserpadmin/addsalesorders.html', {'today': today})
    
    if request.method == 'POST':
        # ============ CALCULATION LOGIC FOR SAVE BUTTON ============
        # Check if it's JSON request (from Save button)
        if request.content_type == 'application/json':
            try:
                print("🔢 SALES ORDER CALCULATION REQUEST from Save button")
                data = json.loads(request.body)
                
                line_items = data.get('line_items', [])
                round_off = float(data.get('round_off', 0))
                
                print(f"📦 Sales Order Calculation data - Items: {len(line_items)}, Round Off: {round_off}")
                
                calculated_items = []
                taxable_total = 0
                cgst_total = 0
                sgst_total = 0
                igst_total = 0
                cess_total = 0
                total_amount = 0
                
                # Perform calculation for each line item
                for i, item in enumerate(line_items):
                    quantity = float(item.get('quantity', 0))
                    mrp = float(item.get('mrp', 0))
                    discount = float(item.get('discount', 0))
                    hsn_code = item.get('hsn_code', '')
                    
                    print(f"🔍 Processing sales order item {i+1}: Qty={quantity}, MRP={mrp}, Discount={discount}, HSN={hsn_code}")
                    
                    # Get tax rates
                    try:
                        hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
                        tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                        cgst_percent = float(tax_rate.cgst)
                        sgst_percent = float(tax_rate.sgst)
                        igst_percent = float(tax_rate.igst)
                        cess_percent = float(tax_rate.cess)
                        print(f"✅ Tax rates found: CGST={cgst_percent}, SGST={sgst_percent}")
                    except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                        # Use default tax rates
                        cgst_percent = 9
                        sgst_percent = 9
                        igst_percent = 18
                        cess_percent = 0
                        print(f"⚠️ Using default tax rates for HSN: {hsn_code}")
                    
                    # Calculate amounts
                    after_discount = mrp - discount
                    basic_amount = quantity * after_discount
                    cgst_amount = (basic_amount * cgst_percent) / 100
                    sgst_amount = (basic_amount * sgst_percent) / 100
                    igst_amount = (basic_amount * igst_percent) / 100
                    cess_amount = (basic_amount * cess_percent) / 100
                    tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                    final_amount = basic_amount + tax_amount
                    
                    # Round to 2 decimal places
                    calculated_items.append({
                        'basic_amount': round(basic_amount, 2),
                        'tax_amount': round(tax_amount, 2),
                        'final_amount': round(final_amount, 2),
                        'cgst_amount': round(cgst_amount, 2),
                        'sgst_amount': round(sgst_amount, 2),
                        'igst_amount': round(igst_amount, 2),
                        'cess_amount': round(cess_amount, 2),
                    })
                    
                    # Update totals
                    taxable_total += basic_amount
                    cgst_total += cgst_amount
                    sgst_total += sgst_amount
                    igst_total += igst_amount
                    cess_total += cess_amount
                    total_amount += final_amount
                
                # Calculate grand total with round off
                grand_total = total_amount + round_off
                
                # Round totals
                totals = {
                    'taxable_amount': round(taxable_total, 2),
                    'cgst_total': round(cgst_total, 2),
                    'sgst_total': round(sgst_total, 2),
                    'igst_total': round(igst_total, 2),
                    'cess_total': round(cess_total, 2),
                    'grand_total': round(grand_total, 2)
                }
                
                print(f"✅ Sales Order Calculation completed: {totals}")
                
                return JsonResponse({
                    'success': True,
                    'line_items': calculated_items,
                    'totals': totals
                })
                
            except Exception as e:
                print(f"❌ Sales Order Calculation error: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        
        # ============ FORM SUBMISSION LOGIC FOR CREATE BUTTON ============
        else:
            print("💾 SALES ORDER FORM SUBMISSION from Create button")
            
            print("🔍 DEBUG: Starting create_sales_order view")
            print("🔍 DEBUG: POST data:", dict(request.POST))
            
            # Get basic info
            customer_code = request.POST.get('customer_code')
            warehouse_code = request.POST.get('warehouse_code')
            date = request.POST.get('date')
            delivery_date = request.POST.get('delivery_date')
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            payment_terms = request.POST.get('payment_terms', '')
            delivery_terms = request.POST.get('delivery_terms', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            print(f"🔍 DEBUG: Customer Code: {customer_code}")
            print(f"🔍 DEBUG: Warehouse Code: {warehouse_code}")
            
            # Get customer and warehouse objects
            try:
                customer = Customer.objects.get(customer_code=customer_code)
                warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
                print(f"✅ DEBUG: Found customer: {customer.customer_name}")
                print(f"✅ DEBUG: Found warehouse: {warehouse.warehouse_name}")
            except Customer.DoesNotExist:
                messages.error(request, f'Customer with code {customer_code} not found!')
                return redirect('ajserp:addsalesorders')
            except Warehouse.DoesNotExist:
                messages.error(request, f'Warehouse with code {warehouse_code} not found!')
                return redirect('ajserp:addsalesorders')
            
            # Get all line items
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            print(f"🔍 DEBUG: Material names: {material_names}")
            print(f"🔍 DEBUG: Quantities: {quantities}")
            print(f"🔍 DEBUG: HSN Codes: {hsn_codes}")
            
            line_items = []
            total_taxable = 0
            total_cgst = 0
            total_sgst = 0
            total_igst = 0
            total_cess = 0
            total_amount = 0
            
            # SERVER-SIDE CALCULATION (EXACTLY like JavaScript)
            for i in range(len(material_names)):
                if material_names[i]:
                    try:
                        # Get values
                        quantity = float(quantities[i]) if quantities[i] else 0
                        mrp = float(mrps[i]) if mrps[i] else 0
                        discount = float(discounts[i]) if discounts[i] else 0
                        
                        print(f"🔍 DEBUG: Processing material {i+1}: {material_names[i]}")
                        print(f"🔍 DEBUG: Qty: {quantity}, MRP: {mrp}, Discount: {discount}")
                        
                        # Get material object
                        material = Material.objects.get(material_name=material_names[i])
                        
                        # Get tax rates from database - NO FALLBACK, ERROR IF NOT FOUND
                        try:
                            hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                            tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                            cgst_percent = float(tax_rate.cgst)
                            sgst_percent = float(tax_rate.sgst)
                            igst_percent = float(tax_rate.igst)
                            cess_percent = float(tax_rate.cess)
                            print(f"✅ DEBUG: Found tax rates - CGST: {cgst_percent}, SGST: {sgst_percent}, IGST: {igst_percent}, Cess: {cess_percent}")
                        except (HSNCode.DoesNotExist, Taxes.DoesNotExist) as e:
                            messages.error(request, f'Tax rates not found for HSN code: {hsn_codes[i]}')
                            return redirect('ajserp:addsalesorders')
                        
                        # EXACT JAVASCRIPT CALCULATION LOGIC
                        after_discount = mrp - discount
                        basic_amount = quantity * after_discount
                        cgst_amount = (basic_amount * cgst_percent) / 100
                        sgst_amount = (basic_amount * sgst_percent) / 100
                        igst_amount = (basic_amount * igst_percent) / 100
                        cess_amount = (basic_amount * cess_percent) / 100
                        tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                        final_amount = basic_amount + tax_amount
                        
                        # ROUNDING (Same as JavaScript - to 2 decimal places)
                        basic_amount = round(basic_amount, 2)
                        cgst_amount = round(cgst_amount, 2)
                        sgst_amount = round(sgst_amount, 2)
                        igst_amount = round(igst_amount, 2)
                        cess_amount = round(cess_amount, 2)
                        tax_amount = round(tax_amount, 2)
                        final_amount = round(final_amount, 2)
                        
                        print(f"📊 DEBUG: Calculation Results:")
                        print(f"📊 DEBUG: After Discount: {after_discount}")
                        print(f"📊 DEBUG: Basic Amount: {basic_amount}")
                        print(f"📊 DEBUG: CGST Amount: {cgst_amount} ({cgst_percent}%)")
                        print(f"📊 DEBUG: SGST Amount: {sgst_amount} ({sgst_percent}%)")
                        print(f"📊 DEBUG: IGST Amount: {igst_amount} ({igst_percent}%)")
                        print(f"📊 DEBUG: Cess Amount: {cess_amount} ({cess_percent}%)")
                        print(f"📊 DEBUG: Tax Amount: {tax_amount}")
                        print(f"📊 DEBUG: Final Amount: {final_amount}")
                        
                        # Store line item data
                        line_items.append({
                            'material': material,
                            'material_name': material_names[i],
                            'quantity': quantity,
                            'mrp': mrp,
                            'discount': discount,
                            'basic_amount': basic_amount,
                            'cgst_amount': cgst_amount,
                            'sgst_amount': sgst_amount,
                            'igst_amount': igst_amount,
                            'cess_amount': cess_amount,
                            'tax_amount': tax_amount,
                            'final_amount': final_amount,
                            'cgst_rate': cgst_percent,
                            'sgst_rate': sgst_percent,
                            'igst_rate': igst_percent,
                            'cess_rate': cess_percent,
                        })
                        
                        # Update totals
                        total_taxable += basic_amount
                        total_cgst += cgst_amount
                        total_sgst += sgst_amount
                        total_igst += igst_amount
                        total_cess += cess_amount
                        total_amount += final_amount
                        
                    except Material.DoesNotExist:
                        messages.error(request, f'Material "{material_names[i]}" not found!')
                        return redirect('ajserp:addsalesorders')
                    except Exception as e:
                        messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                        return redirect('ajserp:addsalesorders')
            
            # Calculate grand total with round off
            grand_total = total_amount + round_off
            
            # Round totals to 2 decimal places (same as JavaScript)
            total_taxable = round(total_taxable, 2)
            total_cgst = round(total_cgst, 2)
            total_sgst = round(total_sgst, 2)
            total_igst = round(total_igst, 2)
            total_cess = round(total_cess, 2)
            total_amount = round(total_amount, 2)
            grand_total = round(grand_total, 2)
            
            print(f"🎯 DEBUG: Final Totals:")
            print(f"🎯 DEBUG: Taxable Amount: {total_taxable}")
            print(f"🎯 DEBUG: CGST Total: {total_cgst}")
            print(f"🎯 DEBUG: SGST Total: {total_sgst}")
            print(f"🎯 DEBUG: IGST Total: {total_igst}")
            print(f"🎯 DEBUG: Cess Total: {total_cess}")
            print(f"🎯 DEBUG: Total Amount: {total_amount}")
            print(f"🎯 DEBUG: Round Off: {round_off}")
            print(f"🎯 DEBUG: Grand Total: {grand_total}")
            
            # Create Sales Order
            sales_order = SalesOrder.objects.create(
                customer=customer,
                warehouse=warehouse,
                date=date,
                delivery_date=delivery_date,
                ref_number=ref_number,
                description=description,
                terms_conditions=terms_conditions,
                billing_address1=billing_address1,
                billing_address2=billing_address2,
                billing_city=billing_city,
                billing_state=billing_state,
                billing_postal_code=billing_postal_code,
                payment_terms=payment_terms,
                delivery_terms=delivery_terms,
                taxable_amount=total_taxable,
                cgst=total_cgst,
                sgst=total_sgst,
                igst=total_igst,
                cess=total_cess,
                round_off=round_off,
                grand_total=grand_total,
                created_by=request.user
            )
            
            # Create Sales Order Items
            for i, item_data in enumerate(line_items):
                SalesOrderItem.objects.create(
                    sales_order=sales_order,
                    material=item_data['material'],
                    material_name=item_data['material_name'],
                    quantity=item_data['quantity'],
                    mrp=item_data['mrp'],
                    discount=item_data['discount'],
                    amount=item_data['basic_amount'],
                    sgst_rate=item_data['sgst_rate'],
                    cgst_rate=item_data['cgst_rate'],
                    igst_rate=item_data['igst_rate'],
                    cess_rate=item_data['cess_rate'],
                    sgst_amount=item_data['sgst_amount'],
                    cgst_amount=item_data['cgst_amount'],
                    igst_amount=item_data['igst_amount'],
                    cess_amount=item_data['cess_amount'],
                    sequence=i + 1
                )
            
            # Final verification with model method
            sales_order.calculate_totals()
            
            messages.success(request, f'Sales Order created successfully! Order Number: {sales_order.order_number}')
            return redirect('ajserp:salesorders')

@login_required
def salesorders(request):
    """Display list of all sales orders"""
    sales_orders = SalesOrder.objects.all().order_by('-date').prefetch_related('sales_order_items')
    
    # Get filter parameters
    order_number = request.GET.get('order_number', '')
    customer_name = request.GET.get('customer_name', '')
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    q = request.GET.get('q', '')  # Global search parameter
    
    # Apply filters
    if order_number:
        sales_orders = sales_orders.filter(order_number__icontains=order_number)
    if customer_name:
        sales_orders = sales_orders.filter(customer__customer_name__icontains=customer_name)
    if status:
        sales_orders = sales_orders.filter(status=status)
    if from_date:
        sales_orders = sales_orders.filter(date__gte=from_date)
    if to_date:
        sales_orders = sales_orders.filter(date__lte=to_date)
        
    # Global search (search across multiple fields)
    if q:
        sales_orders = sales_orders.filter(
            models.Q(order_number__icontains=q) |
            models.Q(customer__customer_name__icontains=q) |
            models.Q(billing_city__icontains=q) |
            models.Q(ref_number__icontains=q)
        )
        
    # Pagination - Show 10 sales orders per page
    paginator = Paginator(sales_orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "ajserpadmin/salesorders.html", {
        'sales_orders': page_obj,
        'page_obj': page_obj,
    })

@login_required
def edit_sales_order(request, order_id):
    """Edit an existing sales order"""
    sales_order = get_object_or_404(SalesOrder, id=order_id)
    
    if request.method == 'POST':
        try:
            print(f"🔧 EDITING SALES ORDER {sales_order.order_number}")
            print("📝 POST data:", dict(request.POST))
            
            # Get basic info
            customer_id = request.POST.get('customer')
            date = request.POST.get('date')
            delivery_date = request.POST.get('delivery_date')
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            payment_terms = request.POST.get('payment_terms', '')
            delivery_terms = request.POST.get('delivery_terms', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            # Get customer
            customer = get_object_or_404(Customer, id=customer_id)
            
            # Update sales order fields
            sales_order.customer = customer
            sales_order.date = date
            sales_order.delivery_date = delivery_date
            sales_order.ref_number = ref_number
            sales_order.description = description
            sales_order.terms_conditions = terms_conditions
            sales_order.billing_address1 = billing_address1
            sales_order.billing_address2 = billing_address2
            sales_order.billing_city = billing_city
            sales_order.billing_state = billing_state
            sales_order.billing_postal_code = billing_postal_code
            sales_order.payment_terms = payment_terms
            sales_order.delivery_terms = delivery_terms
            sales_order.round_off = round_off
            
            # Handle line items if provided
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            if material_names and material_names[0]:  # If items are provided
                # Delete existing items
                sales_order.sales_order_items.all().delete()
                
                # Create new items
                for i in range(len(material_names)):
                    if material_names[i]:
                        try:
                            material = Material.objects.get(material_name=material_names[i])
                            
                            quantity = float(quantities[i]) if quantities[i] else 0
                            mrp = float(mrps[i]) if mrps[i] else 0
                            discount = float(discounts[i]) if discounts[i] else 0
                            
                            # Get tax rates
                            try:
                                hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                                tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                                cgst_percent = float(tax_rate.cgst)
                                sgst_percent = float(tax_rate.sgst)
                                igst_percent = float(tax_rate.igst)
                                cess_percent = float(tax_rate.cess)
                            except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                                # Use default tax rates if not found
                                cgst_percent = 9
                                sgst_percent = 9
                                igst_percent = 18
                                cess_percent = 0
                            
                            # Calculate amounts
                            after_discount = mrp - discount
                            basic_amount = quantity * after_discount
                            cgst_amount = (basic_amount * cgst_percent) / 100
                            sgst_amount = (basic_amount * sgst_percent) / 100
                            igst_amount = (basic_amount * igst_percent) / 100
                            cess_amount = (basic_amount * cess_percent) / 100
                            tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                            final_amount = basic_amount + tax_amount
                            
                            # Create sales order item
                            SalesOrderItem.objects.create(
                                sales_order=sales_order,
                                material=material,
                                material_name=material_names[i],
                                quantity=quantity,
                                mrp=mrp,
                                discount=discount,
                                amount=round(basic_amount, 2),
                                sgst_rate=sgst_percent,
                                cgst_rate=cgst_percent,
                                igst_rate=igst_percent,
                                cess_rate=cess_percent,
                                sgst_amount=round(sgst_amount, 2),
                                cgst_amount=round(cgst_amount, 2),
                                igst_amount=round(igst_amount, 2),
                                cess_amount=round(cess_amount, 2),
                                sequence=i + 1
                            )
                            
                        except Material.DoesNotExist:
                            messages.error(request, f'Material "{material_names[i]}" not found!')
                            return redirect('ajserp:salesorders')
                        except Exception as e:
                            messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                            return redirect('ajserp:salesorders')
            
            # Recalculate totals
            sales_order.calculate_totals()
            sales_order.save()
            
            messages.success(request, f'Sales Order {sales_order.order_number} updated successfully!')
            return redirect('ajserp:salesorders')
            
        except Exception as e:
            print(f"❌ Error updating sales order: {str(e)}")
            messages.error(request, f'Error updating sales order: {str(e)}')
            return redirect('ajserp:salesorders')
    
    # For GET request, redirect to sales orders list
    return redirect('ajserp:salesorders')

@login_required
def delete_sales_order(request, order_id):
    """Delete a sales order"""
    if request.method == 'POST':
        try:
            sales_order = get_object_or_404(SalesOrder, id=order_id)
            order_number = sales_order.order_number
            sales_order.delete()
            messages.success(request, f'Sales Order {order_number} deleted successfully!')
        except SalesOrder.DoesNotExist:
            messages.error(request, 'Sales Order not found!')
        except Exception as e:
            messages.error(request, f'Error deleting sales order: {str(e)}')
    
    return redirect('ajserp:salesorders')

# API Views for Sales Order
@login_required
def get_sales_order_suggestions(request):
    """Get sales order number suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 SALES ORDER SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        sales_orders = SalesOrder.objects.filter(
            order_number__icontains=query
        ).values('order_number', 'customer__customer_name')[:10]
        
        suggestions = []
        for order in sales_orders:
            suggestions.append({
                'value': order['order_number'],
                'text': f"{order['order_number']} - {order['customer__customer_name']}"
            })
        
        print(f"✅ Found {len(suggestions)} sales order suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_sales_order_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_sales_order_global_suggestions(request):
    """Get global search suggestions for sales orders"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 SALES ORDER GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search sales order numbers
        sales_orders = SalesOrder.objects.filter(order_number__icontains=query)[:5]
        for order in sales_orders:
            suggestions.append({
                'value': order.order_number,
                'text': f"Sales Order: {order.order_number} - {order.customer.customer_name}"
            })
        
        # Search customer names  
        customers = Customer.objects.filter(customer_name__icontains=query)[:5]
        for cust in customers:
            suggestions.append({
                'value': cust.customer_name,
                'text': f"Customer: {cust.customer_name}"
            })
        
        print(f"✅ Found {len(suggestions)} sales order global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_sales_order_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    
@login_required
def create_sales_order(request):
    
    if request.method == 'GET':
        from datetime import date
        today = date.today().isoformat()
        return render(request, 'ajserpadmin/addsalesorders.html', {'today': today})
    
    if request.method == 'POST':
        # ============ CALCULATION LOGIC FOR SAVE BUTTON ============
        # Check if it's JSON request (from Save button)
        if request.content_type == 'application/json':
            try:
                print("🔢 SALES ORDER CALCULATION REQUEST from Save button")
                data = json.loads(request.body)
                
                line_items = data.get('line_items', [])
                round_off = float(data.get('round_off', 0))
                
                print(f"📦 Sales Order Calculation data - Items: {len(line_items)}, Round Off: {round_off}")
                
                calculated_items = []
                taxable_total = 0
                cgst_total = 0
                sgst_total = 0
                igst_total = 0
                cess_total = 0
                total_amount = 0
                
                # Perform calculation for each line item
                for i, item in enumerate(line_items):
                    quantity = float(item.get('quantity', 0))
                    mrp = float(item.get('mrp', 0))
                    discount = float(item.get('discount', 0))
                    hsn_code = item.get('hsn_code', '')
                    
                    print(f"🔍 Processing sales order item {i+1}: Qty={quantity}, MRP={mrp}, Discount={discount}, HSN={hsn_code}")
                    
                    # Get tax rates
                    try:
                        hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
                        tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                        cgst_percent = float(tax_rate.cgst)
                        sgst_percent = float(tax_rate.sgst)
                        igst_percent = float(tax_rate.igst)
                        cess_percent = float(tax_rate.cess)
                        print(f"✅ Tax rates found: CGST={cgst_percent}, SGST={sgst_percent}")
                    except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                        # Use default tax rates
                        cgst_percent = 9
                        sgst_percent = 9
                        igst_percent = 18
                        cess_percent = 0
                        print(f"⚠️ Using default tax rates for HSN: {hsn_code}")
                    
                    # Calculate amounts
                    after_discount = mrp - discount
                    basic_amount = quantity * after_discount
                    cgst_amount = (basic_amount * cgst_percent) / 100
                    sgst_amount = (basic_amount * sgst_percent) / 100
                    igst_amount = (basic_amount * igst_percent) / 100
                    cess_amount = (basic_amount * cess_percent) / 100
                    tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                    final_amount = basic_amount + tax_amount
                    
                    # Round to 2 decimal places
                    calculated_items.append({
                        'basic_amount': round(basic_amount, 2),
                        'tax_amount': round(tax_amount, 2),
                        'final_amount': round(final_amount, 2),
                        'cgst_amount': round(cgst_amount, 2),
                        'sgst_amount': round(sgst_amount, 2),
                        'igst_amount': round(igst_amount, 2),
                        'cess_amount': round(cess_amount, 2),
                    })
                    
                    # Update totals
                    taxable_total += basic_amount
                    cgst_total += cgst_amount
                    sgst_total += sgst_amount
                    igst_total += igst_amount
                    cess_total += cess_amount
                    total_amount += final_amount
                
                # Calculate grand total with round off
                grand_total = total_amount + round_off
                
                # Round totals
                totals = {
                    'taxable_amount': round(taxable_total, 2),
                    'cgst_total': round(cgst_total, 2),
                    'sgst_total': round(sgst_total, 2),
                    'igst_total': round(igst_total, 2),
                    'cess_total': round(cess_total, 2),
                    'grand_total': round(grand_total, 2)
                }
                
                print(f"✅ Sales Order Calculation completed: {totals}")
                
                return JsonResponse({
                    'success': True,
                    'line_items': calculated_items,
                    'totals': totals
                })
                
            except Exception as e:
                print(f"❌ Sales Order Calculation error: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        
        # ============ FORM SUBMISSION LOGIC FOR CREATE BUTTON ============
        else:
            print("💾 SALES ORDER FORM SUBMISSION from Create button")
            
            # YOUR EXISTING FORM SUBMISSION CODE FOR SALES ORDER
            print("🔍 DEBUG: Starting create_sales_order view")
            print("🔍 DEBUG: POST data:", dict(request.POST))
            
            # Get basic info
            customer_code = request.POST.get('customer_code')
            warehouse_code = request.POST.get('warehouse_code')
            date = request.POST.get('date')
            delivery_date = request.POST.get('delivery_date')  # Sales Order specific
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            print(f"🔍 DEBUG: Customer Code: {customer_code}")
            print(f"🔍 DEBUG: Warehouse Code: {warehouse_code}")
            
            # Get customer and warehouse objects
            try:
                customer = Customer.objects.get(customer_code=customer_code)
                warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
                print(f"✅ DEBUG: Found customer: {customer.customer_name}")
                print(f"✅ DEBUG: Found warehouse: {warehouse.warehouse_name}")
            except Customer.DoesNotExist:
                messages.error(request, f'Customer with code {customer_code} not found!')
                return redirect('ajserp:addsalesorders')
            except Warehouse.DoesNotExist:
                messages.error(request, f'Warehouse with code {warehouse_code} not found!')
                return redirect('ajserp:addsalesorders')
            
            # Get all line items
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            print(f"🔍 DEBUG: Material names: {material_names}")
            print(f"🔍 DEBUG: Quantities: {quantities}")
            print(f"🔍 DEBUG: HSN Codes: {hsn_codes}")
            
            line_items = []
            total_taxable = 0
            total_cgst = 0
            total_sgst = 0
            total_igst = 0
            total_cess = 0
            total_amount = 0
            
            # SERVER-SIDE CALCULATION (EXACTLY like JavaScript)
            for i in range(len(material_names)):
                if material_names[i]:
                    try:
                        # Get values
                        quantity = float(quantities[i]) if quantities[i] else 0
                        mrp = float(mrps[i]) if mrps[i] else 0
                        discount = float(discounts[i]) if discounts[i] else 0
                        
                        print(f"🔍 DEBUG: Processing material {i+1}: {material_names[i]}")
                        print(f"🔍 DEBUG: Qty: {quantity}, MRP: {mrp}, Discount: {discount}")
                        
                        # Get material object
                        material = Material.objects.get(material_name=material_names[i])
                        
                        # Get tax rates from database - NO FALLBACK, ERROR IF NOT FOUND
                        try:
                            hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                            tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                            cgst_percent = float(tax_rate.cgst)
                            sgst_percent = float(tax_rate.sgst)
                            igst_percent = float(tax_rate.igst)
                            cess_percent = float(tax_rate.cess)
                            print(f"✅ DEBUG: Found tax rates - CGST: {cgst_percent}, SGST: {sgst_percent}, IGST: {igst_percent}, Cess: {cess_percent}")
                        except (HSNCode.DoesNotExist, Taxes.DoesNotExist) as e:
                            messages.error(request, f'Tax rates not found for HSN code: {hsn_codes[i]}')
                            return redirect('ajserp:addsalesorders')
                        
                        # EXACT JAVASCRIPT CALCULATION LOGIC
                        # After_Discount = MRP - Discount
                        # Line_basic = Quantity × After_Discount
                        # Line_CGST_Amt = Line_basic x CGST / 100
                        # Line_SGST_Amt = Line_basic x SGST / 100
                        # Line_IGST_Amt = Line_basic x IGST / 100
                        # Line_Cess_Amt = Line_basic x Cess / 100
                        # Line_Tax = Line_CGST_Amt + Line_SGST_Amt + Line_IGST_Amt + Line_Cess_Amt
                        # Line_Amount = Line_basic + Line_Tax
                        
                        # Step 1: After Discount
                        after_discount = mrp - discount
                        
                        # Step 2: Line Basic Amount (Taxable Amount)
                        basic_amount = quantity * after_discount
                        
                        # Step 3: Calculate individual tax amounts
                        cgst_amount = (basic_amount * cgst_percent) / 100
                        sgst_amount = (basic_amount * sgst_percent) / 100
                        igst_amount = (basic_amount * igst_percent) / 100
                        cess_amount = (basic_amount * cess_percent) / 100
                        
                        # Step 4: Total Tax Amount
                        tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                        
                        # Step 5: Final Line Amount
                        final_amount = basic_amount + tax_amount
                        
                        # ROUNDING (Same as JavaScript - to 2 decimal places)
                        basic_amount = round(basic_amount, 2)
                        cgst_amount = round(cgst_amount, 2)
                        sgst_amount = round(sgst_amount, 2)
                        igst_amount = round(igst_amount, 2)
                        cess_amount = round(cess_amount, 2)
                        tax_amount = round(tax_amount, 2)
                        final_amount = round(final_amount, 2)
                        
                        print(f"📊 DEBUG: Calculation Results:")
                        print(f"📊 DEBUG: After Discount: {after_discount}")
                        print(f"📊 DEBUG: Basic Amount: {basic_amount}")
                        print(f"📊 DEBUG: CGST Amount: {cgst_amount} ({cgst_percent}%)")
                        print(f"📊 DEBUG: SGST Amount: {sgst_amount} ({sgst_percent}%)")
                        print(f"📊 DEBUG: IGST Amount: {igst_amount} ({igst_percent}%)")
                        print(f"📊 DEBUG: Cess Amount: {cess_amount} ({cess_percent}%)")
                        print(f"📊 DEBUG: Tax Amount: {tax_amount}")
                        print(f"📊 DEBUG: Final Amount: {final_amount}")
                        
                        # Store line item data
                        line_items.append({
                            'material': material,
                            'material_name': material_names[i],
                            'quantity': quantity,
                            'mrp': mrp,
                            'discount': discount,
                            'basic_amount': basic_amount,
                            'cgst_amount': cgst_amount,
                            'sgst_amount': sgst_amount,
                            'igst_amount': igst_amount,
                            'cess_amount': cess_amount,
                            'tax_amount': tax_amount,
                            'final_amount': final_amount,
                            'cgst_rate': cgst_percent,
                            'sgst_rate': sgst_percent,
                            'igst_rate': igst_percent,
                            'cess_rate': cess_percent,
                        })
                        
                        # Update totals
                        total_taxable += basic_amount
                        total_cgst += cgst_amount
                        total_sgst += sgst_amount
                        total_igst += igst_amount
                        total_cess += cess_amount
                        total_amount += final_amount
                        
                    except Material.DoesNotExist:
                        messages.error(request, f'Material "{material_names[i]}" not found!')
                        return redirect('ajserp:addsalesorders')
                    except Exception as e:
                        messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                        return redirect('ajserp:addsalesorders')
            
            # Calculate grand total with round off
            grand_total = total_amount + round_off
            
            # Round totals to 2 decimal places (same as JavaScript)
            total_taxable = round(total_taxable, 2)
            total_cgst = round(total_cgst, 2)
            total_sgst = round(total_sgst, 2)
            total_igst = round(total_igst, 2)
            total_cess = round(total_cess, 2)
            total_amount = round(total_amount, 2)
            grand_total = round(grand_total, 2)
            
            print(f"🎯 DEBUG: Final Totals:")
            print(f"🎯 DEBUG: Taxable Amount: {total_taxable}")
            print(f"🎯 DEBUG: CGST Total: {total_cgst}")
            print(f"🎯 DEBUG: SGST Total: {total_sgst}")
            print(f"🎯 DEBUG: IGST Total: {total_igst}")
            print(f"🎯 DEBUG: Cess Total: {total_cess}")
            print(f"🎯 DEBUG: Total Amount: {total_amount}")
            print(f"🎯 DEBUG: Round Off: {round_off}")
            print(f"🎯 DEBUG: Grand Total: {grand_total}")
            
            # Create Sales Order (You'll need to create SalesOrder model similar to Estimate)
            # For now, I'll show how it would work with a SalesOrder model
            try:
                from .models import SalesOrder, SalesOrderItem  # Import your sales order models
                
                sales_order = SalesOrder.objects.create(
                    customer=customer,
                    warehouse=warehouse,
                    date=date,
                    delivery_date=delivery_date,
                    ref_number=ref_number,
                    description=description,
                    terms_conditions=terms_conditions,
                    billing_address1=billing_address1,
                    billing_address2=billing_address2,
                    billing_city=billing_city,
                    billing_state=billing_state,
                    billing_postal_code=billing_postal_code,
                    taxable_amount=total_taxable,
                    cgst=total_cgst,
                    sgst=total_sgst,
                    igst=total_igst,
                    cess=total_cess,
                    round_off=round_off,
                    grand_total=grand_total,
                    created_by=request.user
                )
                
                # Create Sales Order Items
                for i, item_data in enumerate(line_items):
                    SalesOrderItem.objects.create(
                        sales_order=sales_order,
                        material=item_data['material'],
                        material_name=item_data['material_name'],
                        quantity=item_data['quantity'],
                        mrp=item_data['mrp'],
                        discount=item_data['discount'],
                        amount=item_data['basic_amount'],
                        sgst_rate=item_data['sgst_rate'],
                        cgst_rate=item_data['cgst_rate'],
                        igst_rate=item_data['igst_rate'],
                        cess_rate=item_data['cess_rate'],
                        sgst_amount=item_data['sgst_amount'],
                        cgst_amount=item_data['cgst_amount'],
                        igst_amount=item_data['igst_amount'],
                        cess_amount=item_data['cess_amount'],
                        sequence=i + 1
                    )
                
                messages.success(request, f'Sales Order created successfully! Order Number: {sales_order.order_number}')
                return redirect('ajserp:salesorders')
                
            except Exception as e:
                print(f"❌ Error creating sales order: {str(e)}")
                messages.error(request, f'Error creating sales order: {str(e)}')
                return redirect('ajserp:addsalesorders')
            

# @login_required
# def addsalesinvoice(request):
#     """Create Sales Invoice"""

#     if request.method == 'POST':
#         print("\n========== SALES INVOICE CREATE ==========\n")

#         # Basic fields
#         customer_code = request.POST.get('customer_code')
#         warehouse_code = request.POST.get('warehouse_code')
#         date = request.POST.get('date')
#         ref_number = request.POST.get('ref_number', '')
#         description = request.POST.get('description', '')
#         terms_conditions = request.POST.get('terms_conditions', '')

#         # Billing address
#         billing_address1 = request.POST.get('billing_address1', '')
#         billing_address2 = request.POST.get('billing_address2', '')
#         billing_city = request.POST.get('billing_city', '')
#         billing_state = request.POST.get('billing_state', '')
#         billing_postal_code = request.POST.get('billing_postal_code', '')

#         # Round off
#         round_off = float(request.POST.get('round_off', 0))

#         # Fetch objects
#         try:
#             customer = Customer.objects.get(customer_code=customer_code)
#             warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
#         except:
#             messages.error(request, "Invalid Customer or Warehouse")
#             return redirect("ajserp:addsalesinvoice")

#         # Line arrays
#         material_names = request.POST.getlist('material_name[]')
#         quantities = request.POST.getlist('quantity[]')
#         mrps = request.POST.getlist('mrp[]')
#         discounts = request.POST.getlist('discount[]')
#         hsn_codes = request.POST.getlist('hsn_code[]')

#         line_items = []

#         total_taxable = 0
#         total_cgst = 0
#         total_sgst = 0
#         total_igst = 0
#         total_cess = 0
#         total_amount = 0

#         # PROCESS EACH LINE ITEM
#         for i in range(len(material_names)):

#             if not material_names[i]:
#                 continue

#             quantity = float(quantities[i])
#             mrp = float(mrps[i])
#             discount = float(discounts[i])
#             hsn_code = hsn_codes[i]

#             # BASIC AMOUNT
#             basic_amount = quantity * mrp
#             total_taxable += basic_amount

#             # FETCH TAX RATE FROM Taxes TABLE (correct source)
#             try:
#                 hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
#                 tax = Taxes.objects.get(hsn_code=hsn_obj)

#                 cgst_rate = float(tax.cgst)
#                 sgst_rate = float(tax.sgst)
#                 igst_rate = float(tax.igst)
#                 cess_rate = float(tax.cess)

#             except:
#                 messages.error(request, f"Tax rates for HSN {hsn_code} not found!")
#                 return redirect("ajserp:addsalesinvoice")

#             # TAX CALCULATION — BOSS LOGIC (float)
#             cgst_amount = (basic_amount * cgst_rate) / 100
#             sgst_amount = (basic_amount * sgst_rate) / 100
#             igst_amount = (basic_amount * igst_rate) / 100
#             cess_amount = (basic_amount * cess_rate) / 100

#             # TOTAL OF EACH LINE
#             line_total = basic_amount + cgst_amount + sgst_amount + igst_amount + cess_amount

#             # Add to totals
#             total_cgst += cgst_amount
#             total_sgst += sgst_amount
#             total_igst += igst_amount
#             total_cess += cess_amount
#             total_amount += line_total

#             # Material object
#             material = Material.objects.get(material_name=material_names[i])

#             # Store line item
#             line_items.append({
#                 "material": material,
#                 "material_name": material_names[i],
#                 "quantity": quantity,
#                 "mrp": mrp,
#                 "basic_amount": basic_amount,
#                 "cgst_rate": cgst_rate,
#                 "sgst_rate": sgst_rate,
#                 "igst_rate": igst_rate,
#                 "cess_rate": cess_rate,
#                 "cgst_amount": cgst_amount,
#                 "sgst_amount": sgst_amount,
#                 "igst_amount": igst_amount,
#                 "cess_amount": cess_amount,
#                 "line_total": line_total,
#             })

#         # GRAND TOTAL
#         # grand_total = round(total_amount + round_off)
#         # ✔ ROUND CORRECTLY LIKE 3204.60 → 3205
#         final_rounded_total = round(total_amount)

# # ✔ Grand total is rounded value + round_off
#         grand_total = final_rounded_total + round_off


#         # CREATE INVOICE
#         sales_invoice = SalesInvoice.objects.create(
#             customer=customer,
#             warehouse=warehouse,
#             date=date,
#             ref_number=ref_number,
#             description=description,
#             terms_conditions=terms_conditions,
#             billing_address1=billing_address1,
#             billing_address2=billing_address2,
#             billing_city=billing_city,
#             billing_state=billing_state,
#             billing_postal_code=billing_postal_code,
#             taxable_amount=total_taxable,
#             cgst=total_cgst,
#             sgst=total_sgst,
#             igst=total_igst,
#             cess=total_cess,
#             round_off=round_off,
#             grand_total=grand_total,
#             created_by=request.user
#         )

#         # SAVE ITEMS
#         for idx, item in enumerate(line_items):
#             SalesInvoiceItem.objects.create(
#                 sales_invoice=sales_invoice,
#                 material=item["material"],
#                 material_name=item["material_name"],
#                 quantity=item["quantity"],
#                 mrp=item["mrp"],
#                 amount=item["basic_amount"],
#                 cgst_rate=item["cgst_rate"],
#                 sgst_rate=item["sgst_rate"],
#                 igst_rate=item["igst_rate"],
#                 cess_rate=item["cess_rate"],
#                 cgst_amount=item["cgst_amount"],
#                 sgst_amount=item["sgst_amount"],
#                 igst_amount=item["igst_amount"],
#                 cess_amount=item["cess_amount"],
#                 sequence=idx + 1
#             )

#         messages.success(request, f"Invoice created successfully!")
#         return redirect("ajserp:salesinvoice")

#     # GET request
#     materials = Material.objects.all()
#     customers = Customer.objects.all()
#     warehouses = Warehouse.objects.all()

#     return render(request, "ajserpadmin/addsalesinvoice.html", {
#         "materials": materials,
#         "customers": customers,
#         "warehouses": warehouses,
#         "today": datetime.now().date()
#     })


# @login_required
# def create_sales_invoice(request):
#     """Handle calculation from Save button (AJAX JSON)"""

#     if request.method == 'POST' and request.content_type == 'application/json':
#         try:
#             print("🔢 SALES INVOICE CALCULATION REQUEST")
#             data = json.loads(request.body)

#             line_items = data.get('line_items', [])
#             round_off = float(data.get('round_off', 0))

#             calculated_items = []
#             taxable_total = 0
#             cgst_total = 0
#             sgst_total = 0
#             igst_total = 0
#             cess_total = 0
#             total_amount = 0

#             for i, item in enumerate(line_items):

#                 quantity = float(item.get('quantity', 0))
#                 mrp = float(item.get('mrp', 0))
#                 discount = float(item.get('discount', 0))
#                 hsn_code = item.get('hsn_code', '')

#                 print(f"🔍 Line {i+1}: Qty={quantity}, MRP={mrp}, HSN={hsn_code}")

#                 # 1️⃣ Fetch tax rates from Taxes table
#                 try:
#                     tax = Taxes.objects.get(hsn_code__hsn_code=hsn_code)
#                 except Taxes.DoesNotExist:
#                     return JsonResponse({
#                         "success": False,
#                         "error": f"Tax rates not found for HSN {hsn_code}"
#                     })

#                 # Extract percentages
#                 cgst_percent = float(tax.cgst)
#                 sgst_percent = float(tax.sgst)
#                 igst_percent = float(tax.igst)
#                 cess_percent = float(tax.cess)

#                 # 2️⃣ Basic calculation
#                 after_discount = mrp - discount
#                 basic_amount = quantity * after_discount

#                 # 3️⃣ Tax amounts
#                 cgst_amount = (basic_amount * cgst_percent) / 100
#                 sgst_amount = (basic_amount * sgst_percent) / 100
#                 igst_amount = (basic_amount * igst_percent) / 100
#                 cess_amount = (basic_amount * cess_percent) / 100

#                 tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
#                 final_amount = basic_amount + tax_amount

#                 # 4️⃣ Add line calculations
#                 calculated_items.append({
#                     "basic_amount": round(basic_amount, 2),
#                     "tax_amount": round(tax_amount, 2),
#                     "final_amount": round(final_amount, 2),
#                     "cgst_amount": round(cgst_amount, 2),
#                     "sgst_amount": round(sgst_amount, 2),
#                     "igst_amount": round(igst_amount, 2),
#                     "cess_amount": round(cess_amount, 2),
#                 })

#                 # 5️⃣ Add to totals
#                 taxable_total += basic_amount
#                 cgst_total += cgst_amount
#                 sgst_total += sgst_amount
#                 igst_total += igst_amount
#                 cess_total += cess_amount
#                 total_amount += final_amount

#             # # 6️⃣ Grand Total
#             # grand_total = round(total_amount + round_off)
#             # ✔ ROUND CORRECTLY LIKE 3204.60 → 3205
#             final_rounded_total = round(total_amount)

# # ✔ Grand total is rounded value + round_off
#             grand_total = final_rounded_total + round_off


#             totals = {
#                 "taxable_amount": round(taxable_total, 2),
#                 "cgst_total": round(cgst_total, 2),
#                 "sgst_total": round(sgst_total, 2),
#                 "igst_total": round(igst_total, 2),
#                 "cess_total": round(cess_total, 2),
#                 "grand_total": round(grand_total, 2)
#             }

#             print("✅ Completed:", totals)

#             return JsonResponse({
#                 "success": True,
#                 "line_items": calculated_items,
#                 "totals": totals
#             })

#         except Exception as e:
#             print(f"❌ Error: {str(e)}")
#             return JsonResponse({"success": False, "error": str(e)})

#     return redirect("ajserp:addsalesinvoice")

@login_required
def addsalesinvoice(request):
    """Create Sales Invoice"""

    if request.method == 'POST':
        print("\n========== SALES INVOICE CREATE ==========\n")

        # Basic fields
        customer_code = request.POST.get('customer_code')
        warehouse_code = request.POST.get('warehouse_code')
        date = request.POST.get('date')
        ref_number = request.POST.get('ref_number', '')
        description = request.POST.get('description', '')
        terms_conditions = request.POST.get('terms_conditions', '')

        # Billing address
        billing_address1 = request.POST.get('billing_address1', '')
        billing_address2 = request.POST.get('billing_address2', '')
        billing_city = request.POST.get('billing_city', '')
        billing_state = request.POST.get('billing_state', '')
        billing_postal_code = request.POST.get('billing_postal_code', '')

        # Round off
        round_off = float(request.POST.get('round_off', 0))

        # Fetch objects
        try:
            customer = Customer.objects.get(customer_code=customer_code)
            warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
        except:
            messages.error(request, "Invalid Customer or Warehouse")
            return redirect("ajserp:addsalesinvoice")

        # Line arrays
        material_names = request.POST.getlist('material_name[]')
        quantities = request.POST.getlist('quantity[]')
        mrps = request.POST.getlist('mrp[]')
        discounts = request.POST.getlist('discount[]')
        hsn_codes = request.POST.getlist('hsn_code[]')

        line_items = []

        total_taxable = 0
        total_cgst = 0
        total_sgst = 0
        total_igst = 0
        total_cess = 0
        total_amount = 0

        # PROCESS EACH LINE ITEM
        for i in range(len(material_names)):

            if not material_names[i]:
                continue

            quantity = float(quantities[i])
            mrp = float(mrps[i])
            discount = float(discounts[i])
            hsn_code = hsn_codes[i]

            # BASIC AMOUNT
            basic_amount = quantity * mrp
            total_taxable += basic_amount

            # FETCH TAX RATE FROM Taxes TABLE
            try:
                hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
                tax = Taxes.objects.get(hsn_code=hsn_obj)

                cgst_rate = float(tax.cgst)
                sgst_rate = float(tax.sgst)
                igst_rate = float(tax.igst)
                cess_rate = float(tax.cess)

            except:
                messages.error(request, f"Tax rates for HSN {hsn_code} not found!")
                return redirect("ajserp:addsalesinvoice")

            # TAX CALCULATION WITH ZERO CHECK
            cgst_amount = (basic_amount * cgst_rate) / 100 if cgst_rate != 0 else 0
            sgst_amount = (basic_amount * sgst_rate) / 100 if sgst_rate != 0 else 0
            igst_amount = (basic_amount * igst_rate) / 100 if igst_rate != 0 else 0
            cess_amount = (basic_amount * cess_rate) / 100 if cess_rate != 0 else 0

            # TOTAL FOR THIS LINE
            line_total = basic_amount + cgst_amount + sgst_amount + igst_amount + cess_amount

            # Add to totals
            total_cgst += cgst_amount
            total_sgst += sgst_amount
            total_igst += igst_amount
            total_cess += cess_amount
            total_amount += line_total

            material = Material.objects.get(material_name=material_names[i])

            # Save line item object
            line_items.append({
                "material": material,
                "material_name": material_names[i],
                "quantity": quantity,
                "mrp": mrp,
                "basic_amount": basic_amount,
                "cgst_rate": cgst_rate,
                "sgst_rate": sgst_rate,
                "igst_rate": igst_rate,
                "cess_rate": cess_rate,
                "cgst_amount": cgst_amount,
                "sgst_amount": sgst_amount,
                "igst_amount": igst_amount,
                "cess_amount": cess_amount,
                "line_total": line_total,
            })

        # ROUNDING LOGIC
        final_rounded_total = round(total_amount)
        grand_total = final_rounded_total + round_off

        # CREATE INVOICE
        sales_invoice = SalesInvoice.objects.create(
            customer=customer,
            warehouse=warehouse,
            date=date,
            ref_number=ref_number,
            description=description,
            terms_conditions=terms_conditions,
            billing_address1=billing_address1,
            billing_address2=billing_address2,
            billing_city=billing_city,
            billing_state=billing_state,
            billing_postal_code=billing_postal_code,
            taxable_amount=total_taxable,
            cgst=total_cgst,
            sgst=total_sgst,
            igst=total_igst,
            cess=total_cess,
            round_off=round_off,
            grand_total=grand_total,
            created_by=request.user
        )

        # SAVE LINE ITEMS
        for idx, item in enumerate(line_items):
            SalesInvoiceItem.objects.create(
                sales_invoice=sales_invoice,
                material=item["material"],
                material_name=item["material_name"],
                quantity=item["quantity"],
                mrp=item["mrp"],
                amount=item["basic_amount"],
                cgst_rate=item["cgst_rate"],
                sgst_rate=item["sgst_rate"],
                igst_rate=item["igst_rate"],
                cess_rate=item["cess_rate"],
                cgst_amount=item["cgst_amount"],
                sgst_amount=item["sgst_amount"],
                igst_amount=item["igst_amount"],
                cess_amount=item["cess_amount"],
                sequence=idx + 1
            )

        messages.success(request, f"Invoice created successfully!")
        return redirect("ajserp:salesinvoice")

    # GET request
    return render(request, "ajserpadmin/addsalesinvoice.html", {
        "materials": Material.objects.all(),
        "customers": Customer.objects.all(),
        "warehouses": Warehouse.objects.all(),
        "today": datetime.now().date()
    })

@login_required
def create_sales_invoice(request):
    """Calculate invoice using AJAX"""

    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            data = json.loads(request.body)

            line_items = data.get('line_items', [])
            round_off = float(data.get('round_off', 0))

            calculated_items = []
            taxable_total = 0
            cgst_total = 0
            sgst_total = 0
            igst_total = 0
            cess_total = 0
            total_amount = 0

            for i, item in enumerate(line_items):

                quantity = float(item.get('quantity', 0))
                mrp = float(item.get('mrp', 0))
                discount = float(item.get('discount', 0))
                hsn_code = item.get('hsn_code', '')

                # Fetch tax from DB
                try:
                    tax = Taxes.objects.get(hsn_code__hsn_code=hsn_code)
                except Taxes.DoesNotExist:
                    return JsonResponse({"success": False, "error": f"Tax rates missing for HSN {hsn_code}"})


                cgst_percent = float(tax.cgst)
                sgst_percent = float(tax.sgst)
                igst_percent = float(tax.igst)
                cess_percent = float(tax.cess)

                # Basic amount after discount
                after_discount = mrp - discount
                basic_amount = quantity * after_discount

                # Tax calculations with zero checks
                cgst_amount = (basic_amount * cgst_percent) / 100 if cgst_percent != 0 else 0
                sgst_amount = (basic_amount * sgst_percent) / 100 if sgst_percent != 0 else 0
                igst_amount = (basic_amount * igst_percent) / 100 if igst_percent != 0 else 0
                cess_amount = (basic_amount * cess_percent) / 100 if cess_percent != 0 else 0

                tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                final_amount = basic_amount + tax_amount

                calculated_items.append({
                    "basic_amount": round(basic_amount, 2),
                    "tax_amount": round(tax_amount, 2),
                    "final_amount": round(final_amount, 2),
                    "cgst_amount": round(cgst_amount, 2),
                    "sgst_amount": round(sgst_amount, 2),
                    "igst_amount": round(igst_amount, 2),
                    "cess_amount": round(cess_amount, 2),
                })

                taxable_total += basic_amount
                cgst_total += cgst_amount
                sgst_total += sgst_amount
                igst_total += igst_amount
                cess_total += cess_amount
                total_amount += final_amount

            # Final rounding
            final_rounded_total = round(total_amount)
            grand_total = final_rounded_total + round_off

            totals = {
                "taxable_amount": round(taxable_total, 2),
                "cgst_total": round(cgst_total, 2),
                "sgst_total": round(sgst_total, 2),
                "igst_total": round(igst_total, 2),
                "cess_total": round(cess_total, 2),
                "grand_total": round(grand_total, 2),
            }

            return JsonResponse({
                "success": True,
                "line_items": calculated_items,
                "totals": totals
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return redirect("ajserp:addsalesinvoice")


@login_required
def salesinvoice(request):
    """Display list of all sales invoices"""
    sales_invoices = SalesInvoice.objects.all().order_by('-date').prefetch_related('sales_invoice_items')
    
    # Get filter parameters
    invoice_number = request.GET.get('invoice_number', '')
    customer_name = request.GET.get('customer_name', '')
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    q = request.GET.get('q', '')  # Global search parameter
    
    # Apply filters
    if invoice_number:
        sales_invoices = sales_invoices.filter(invoice_number__icontains=invoice_number)
    if customer_name:
        sales_invoices = sales_invoices.filter(customer__customer_name__icontains=customer_name)
    if status:
        sales_invoices = sales_invoices.filter(status=status)
    if from_date:
        sales_invoices = sales_invoices.filter(date__gte=from_date)
    if to_date:
        sales_invoices = sales_invoices.filter(date__lte=to_date)
        
    # Global search (search across multiple fields)
    if q:
        sales_invoices = sales_invoices.filter(
            models.Q(invoice_number__icontains=q) |
            models.Q(customer__customer_name__icontains=q) |
            models.Q(billing_city__icontains=q) |
            models.Q(ref_number__icontains=q)
        )
        
    # Pagination - Show 10 sales invoices per page
    paginator = Paginator(sales_invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "ajserpadmin/salesinvoice.html", {
        'sales_invoices': page_obj,
        'page_obj': page_obj,
    })

@login_required
def edit_sales_invoice(request, invoice_id):
    """Edit an existing sales invoice"""
    sales_invoice = get_object_or_404(SalesInvoice, id=invoice_id)
    
    if request.method == 'POST':
        try:
            print(f"🔧 EDITING SALES INVOICE {sales_invoice.invoice_number}")
            print("📝 POST data:", dict(request.POST))
            
            # Get basic info
            customer_id = request.POST.get('customer')
            date = request.POST.get('date')
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            # Get customer
            customer = get_object_or_404(Customer, id=customer_id)
            
            # Update sales invoice fields
            sales_invoice.customer = customer
            sales_invoice.date = date
            sales_invoice.ref_number = ref_number
            sales_invoice.description = description
            sales_invoice.terms_conditions = terms_conditions
            sales_invoice.billing_address1 = billing_address1
            sales_invoice.billing_address2 = billing_address2
            sales_invoice.billing_city = billing_city
            sales_invoice.billing_state = billing_state
            sales_invoice.billing_postal_code = billing_postal_code
            sales_invoice.round_off = round_off
            
            # Handle line items if provided
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            if material_names and material_names[0]:  # If items are provided
                # Delete existing items
                sales_invoice.sales_invoice_items.all().delete()
                
                # Create new items
                for i in range(len(material_names)):
                    if material_names[i]:
                        try:
                            material = Material.objects.get(material_name=material_names[i])
                            
                            quantity = float(quantities[i]) if quantities[i] else 0
                            mrp = float(mrps[i]) if mrps[i] else 0
                            discount = float(discounts[i]) if discounts[i] else 0
                            
                            # Get tax rates
                            try:
                                hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                                tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                                cgst_percent = float(tax_rate.cgst)
                                sgst_percent = float(tax_rate.sgst)
                                igst_percent = float(tax_rate.igst)
                                cess_percent = float(tax_rate.cess)
                            except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                                # Use default tax rates if not found
                                cgst_percent = 9
                                sgst_percent = 9
                                igst_percent = 18
                                cess_percent = 0
                            
                            # Calculate amounts
                            after_discount = mrp - discount
                            basic_amount = quantity * after_discount
                            cgst_amount = (basic_amount * cgst_percent) / 100
                            sgst_amount = (basic_amount * sgst_percent) / 100
                            igst_amount = (basic_amount * igst_percent) / 100
                            cess_amount = (basic_amount * cess_percent) / 100
                            tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                            final_amount = basic_amount + tax_amount
                            
                            # Create sales invoice item
                            SalesInvoiceItem.objects.create(
                                sales_invoice=sales_invoice,
                                material=material,
                                material_name=material_names[i],
                                quantity=quantity,
                                mrp=mrp,
                                discount=discount,
                                amount=round(basic_amount, 2),
                                sgst_rate=sgst_percent,
                                cgst_rate=cgst_percent,
                                igst_rate=igst_percent,
                                cess_rate=cess_percent,
                                sgst_amount=round(sgst_amount, 2),
                                cgst_amount=round(cgst_amount, 2),
                                igst_amount=round(igst_amount, 2),
                                cess_amount=round(cess_amount, 2),
                                sequence=i + 1
                            )
                            
                        except Material.DoesNotExist:
                            messages.error(request, f'Material "{material_names[i]}" not found!')
                            return redirect('ajserp:salesinvoice')
                        except Exception as e:
                            messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                            return redirect('ajserp:salesinvoice')
            
            # Recalculate totals
            sales_invoice.calculate_totals()
            sales_invoice.save()
            
            messages.success(request, f'Sales Invoice {sales_invoice.invoice_number} updated successfully!')
            return redirect('ajserp:salesinvoice')
            
        except Exception as e:
            print(f"❌ Error updating sales invoice: {str(e)}")
            messages.error(request, f'Error updating sales invoice: {str(e)}')
            return redirect('ajserp:salesinvoice')
    
    # For GET request, redirect to sales invoices list
    return redirect('ajserp:salesinvoice')

@login_required
def delete_sales_invoice(request, invoice_id):
    """Delete a sales invoice"""
    if request.method == 'POST':
        try:
            sales_invoice = get_object_or_404(SalesInvoice, id=invoice_id)
            invoice_number = sales_invoice.invoice_number
            sales_invoice.delete()
            messages.success(request, f'Sales Invoice {invoice_number} deleted successfully!')
        except SalesInvoice.DoesNotExist:
            messages.error(request, 'Sales Invoice not found!')
        except Exception as e:
            messages.error(request, f'Error deleting sales invoice: {str(e)}')
    
    return redirect('ajserp:salesinvoices')

# API Views for Sales Invoice
@login_required
def get_sales_invoice_suggestions(request):
    """Get sales invoice number suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 SALES INVOICE SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        sales_invoices = SalesInvoice.objects.filter(
            invoice_number__icontains=query
        ).values('invoice_number', 'customer__customer_name')[:10]
        
        suggestions = []
        for invoice in sales_invoices:
            suggestions.append({
                'value': invoice['invoice_number'],
                'text': f"{invoice['invoice_number']} - {invoice['customer__customer_name']}"
            })
        
        print(f"✅ Found {len(suggestions)} sales invoice suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_sales_invoice_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_sales_invoice_global_suggestions(request):
    """Get global search suggestions for sales invoices"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 SALES INVOICE GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search sales invoice numbers
        sales_invoices = SalesInvoice.objects.filter(invoice_number__icontains=query)[:5]
        for invoice in sales_invoices:
            suggestions.append({
                'value': invoice.invoice_number,
                'text': f"Sales Invoice: {invoice.invoice_number} - {invoice.customer.customer_name}"
            })
        
        # Search customer names  
        customers = Customer.objects.filter(customer_name__icontains=query)[:5]
        for cust in customers:
            suggestions.append({
                'value': cust.customer_name,
                'text': f"Customer: {cust.customer_name}"
            })
        
        print(f"✅ Found {len(suggestions)} sales invoice global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_sales_invoice_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    
@login_required
def addpurchaseorder(request):
    """Display purchase order creation form"""
    if request.method == 'POST':
        try:
            # Create Purchase Order
            purchase_order = PurchaseOrder.objects.create(
                vendor_id=request.POST.get('vendor'),
                warehouse_id=request.POST.get('warehouse'),
                created_by=request.user,
                billing_address1=request.POST.get('billing_address1', ''),
                billing_city=request.POST.get('billing_city', ''),
                billing_state=request.POST.get('billing_state', ''),
                billing_postal_code=request.POST.get('billing_postal_code', ''),
                round_off=request.POST.get('round_off', 0),
                description=request.POST.get('description', ''),
                terms_conditions=request.POST.get('terms_conditions', ''),
                valid_till=request.POST.get('valid_till', '')
            )
            
            # Create Purchase Order Items
            items_data = {}
            for key, value in request.POST.items():
                if key.startswith('items['):
                    # Parse the field name: items[1][quantity] -> index=1, field=quantity
                    parts = key.split('[')
                    if len(parts) >= 3:
                        index = parts[1].replace(']', '')
                        field = parts[2].replace(']', '')
                        
                        if index not in items_data:
                            items_data[index] = {}
                        items_data[index][field] = value
            
            # Create purchase order items
            for index, item_data in items_data.items():
                PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order,
                    material_id=item_data.get('material'),
                    material_name=item_data.get('material_name'),
                    quantity=item_data.get('quantity', 1),
                    mrp=item_data.get('mrp', 0),
                    discount=item_data.get('discount', 0),
                    cgst_rate=item_data.get('cgst_rate', 0),
                    sgst_rate=item_data.get('sgst_rate', 0),
                    igst_rate=item_data.get('igst_rate', 0),
                    cess_rate=item_data.get('cess_rate', 0),
                    sequence=int(index)
                )
            
            # Calculate totals
            purchase_order.calculate_totals()
            
            messages.success(request, f'Purchase Order created successfully! Order Number: {purchase_order.order_number}')
            return redirect('ajserp:purchaseorder')
            
        except Exception as e:
            print(f"Error creating purchase order: {str(e)}")
            messages.error(request, f'Error creating purchase order: {str(e)}')
    
    # GET request - show form
    materials = Material.objects.all()
    vendors = Supplier.objects.all()
    warehouses = Warehouse.objects.all()
    
    context = {
        'materials': materials,
        'vendors': vendors,
        'warehouses': warehouses,
    }
    return render(request, 'ajserpadmin/addpurchaseorder.html', context)

@login_required
def create_purchase_order(request):
    """Handle purchase order creation with calculation logic"""
    
    if request.method == 'GET':
        from datetime import date
        today = date.today().isoformat()
        return render(request, 'ajserpadmin/addpurchaseorder.html', {'today': today})
    
    if request.method == 'POST':
        # ============ CALCULATION LOGIC FOR SAVE BUTTON ============
        if request.content_type == 'application/json':
            try:
                print("🔢 PURCHASE ORDER CALCULATION REQUEST from Save button")
                data = json.loads(request.body)
                
                line_items = data.get('line_items', [])
                round_off = float(data.get('round_off', 0))
                
                print(f"📦 Purchase Order Calculation data - Items: {len(line_items)}, Round Off: {round_off}")
                
                calculated_items = []
                taxable_total = 0
                cgst_total = 0
                sgst_total = 0
                igst_total = 0
                cess_total = 0
                total_amount = 0
                
                # Perform calculation for each line item
                for i, item in enumerate(line_items):
                    quantity = float(item.get('quantity', 0))
                    mrp = float(item.get('mrp', 0))
                    discount = float(item.get('discount', 0))
                    hsn_code = item.get('hsn_code', '')
                    
                    print(f"🔍 Processing purchase order item {i+1}: Qty={quantity}, MRP={mrp}, Discount={discount}, HSN={hsn_code}")
                    
                    # Get tax rates
                    try:
                        hsn_obj = HSNCode.objects.get(hsn_code=hsn_code)
                        tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                        cgst_percent = float(tax_rate.cgst)
                        sgst_percent = float(tax_rate.sgst)
                        igst_percent = float(tax_rate.igst)
                        cess_percent = float(tax_rate.cess)
                        print(f"✅ Tax rates found: CGST={cgst_percent}, SGST={sgst_percent}")
                    except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                        # Use default tax rates
                        cgst_percent = 9
                        sgst_percent = 9
                        igst_percent = 18
                        cess_percent = 0
                        print(f"⚠️ Using default tax rates for HSN: {hsn_code}")
                    
                    # Calculate amounts
                    after_discount = mrp - discount
                    basic_amount = quantity * after_discount
                    cgst_amount = (basic_amount * cgst_percent) / 100
                    sgst_amount = (basic_amount * sgst_percent) / 100
                    igst_amount = (basic_amount * igst_percent) / 100
                    cess_amount = (basic_amount * cess_percent) / 100
                    tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                    final_amount = basic_amount + tax_amount
                    
                    # Round to 2 decimal places
                    calculated_items.append({
                        'basic_amount': round(basic_amount, 2),
                        'tax_amount': round(tax_amount, 2),
                        'final_amount': round(final_amount, 2),
                        'cgst_amount': round(cgst_amount, 2),
                        'sgst_amount': round(sgst_amount, 2),
                        'igst_amount': round(igst_amount, 2),
                        'cess_amount': round(cess_amount, 2),
                    })
                    
                    # Update totals
                    taxable_total += basic_amount
                    cgst_total += cgst_amount
                    sgst_total += sgst_amount
                    igst_total += igst_amount
                    cess_total += cess_amount
                    total_amount += final_amount
                
                # Calculate grand total with round off
                grand_total = total_amount + round_off
                
                # Round totals
                totals = {
                    'taxable_amount': round(taxable_total, 2),
                    'cgst_total': round(cgst_total, 2),
                    'sgst_total': round(sgst_total, 2),
                    'igst_total': round(igst_total, 2),
                    'cess_total': round(cess_total, 2),
                    'grand_total': round(grand_total, 2)
                }
                
                print(f"✅ Purchase Order Calculation completed: {totals}")
                
                return JsonResponse({
                    'success': True,
                    'line_items': calculated_items,
                    'totals': totals
                })
                
            except Exception as e:
                print(f"❌ Purchase Order Calculation error: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        
        # ============ FORM SUBMISSION LOGIC FOR CREATE BUTTON ============
        else:
            print("💾 PURCHASE ORDER FORM SUBMISSION from Create button")
            
            print("🔍 DEBUG: Starting create_purchase_order view")
            print("🔍 DEBUG: POST data:", dict(request.POST))
            
            # Get basic info
            vendor_code = request.POST.get('vendor_code')
            warehouse_code = request.POST.get('warehouse_code')
            date = request.POST.get('date')
            valid_till = request.POST.get('valid_till')
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            print(f"🔍 DEBUG: Vendor Code: {vendor_code}")
            print(f"🔍 DEBUG: Warehouse Code: {warehouse_code}")
            
            # Get vendor and warehouse objects
            try:
                vendor = Supplier.objects.get(vendor_code=vendor_code)
                warehouse = Warehouse.objects.get(warehouse_code=warehouse_code)
                print(f"✅ DEBUG: Found vendor: {vendor.vendor_name}")
                print(f"✅ DEBUG: Found warehouse: {warehouse.warehouse_name}")
            except Supplier.DoesNotExist:
                messages.error(request, f'Vendor with code {vendor_code} not found!')
                return redirect('ajserp:addpurchaseorder')
            except Warehouse.DoesNotExist:
                messages.error(request, f'Warehouse with code {warehouse_code} not found!')
                return redirect('ajserp:addpurchaseorder')
            
            # Get all line items
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            print(f"🔍 DEBUG: Material names: {material_names}")
            print(f"🔍 DEBUG: Quantities: {quantities}")
            print(f"🔍 DEBUG: HSN Codes: {hsn_codes}")
            
            line_items = []
            total_taxable = 0
            total_cgst = 0
            total_sgst = 0
            total_igst = 0
            total_cess = 0
            total_amount = 0
            
            # SERVER-SIDE CALCULATION
            for i in range(len(material_names)):
                if material_names[i]:
                    try:
                        # Get values
                        quantity = float(quantities[i]) if quantities[i] else 0
                        mrp = float(mrps[i]) if mrps[i] else 0
                        discount = float(discounts[i]) if discounts[i] else 0
                        
                        print(f"🔍 DEBUG: Processing material {i+1}: {material_names[i]}")
                        print(f"🔍 DEBUG: Qty: {quantity}, MRP: {mrp}, Discount: {discount}")
                        
                        # Get material object
                        material = Material.objects.get(material_name=material_names[i])
                        
                        # Get tax rates from database
                        try:
                            hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                            tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                            cgst_percent = float(tax_rate.cgst)
                            sgst_percent = float(tax_rate.sgst)
                            igst_percent = float(tax_rate.igst)
                            cess_percent = float(tax_rate.cess)
                            print(f"✅ DEBUG: Found tax rates - CGST: {cgst_percent}, SGST: {sgst_percent}, IGST: {igst_percent}, Cess: {cess_percent}")
                        except (HSNCode.DoesNotExist, Taxes.DoesNotExist) as e:
                            messages.error(request, f'Tax rates not found for HSN code: {hsn_codes[i]}')
                            return redirect('ajserp:addpurchaseorder')
                        
                        # CALCULATION LOGIC
                        after_discount = mrp - discount
                        basic_amount = quantity * after_discount
                        cgst_amount = (basic_amount * cgst_percent) / 100
                        sgst_amount = (basic_amount * sgst_percent) / 100
                        igst_amount = (basic_amount * igst_percent) / 100
                        cess_amount = (basic_amount * cess_percent) / 100
                        tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                        final_amount = basic_amount + tax_amount
                        
                        # ROUNDING to 2 decimal places
                        basic_amount = round(basic_amount, 2)
                        cgst_amount = round(cgst_amount, 2)
                        sgst_amount = round(sgst_amount, 2)
                        igst_amount = round(igst_amount, 2)
                        cess_amount = round(cess_amount, 2)
                        tax_amount = round(tax_amount, 2)
                        final_amount = round(final_amount, 2)
                        
                        print(f"📊 DEBUG: Calculation Results:")
                        print(f"📊 DEBUG: After Discount: {after_discount}")
                        print(f"📊 DEBUG: Basic Amount: {basic_amount}")
                        print(f"📊 DEBUG: CGST Amount: {cgst_amount} ({cgst_percent}%)")
                        print(f"📊 DEBUG: SGST Amount: {sgst_amount} ({sgst_percent}%)")
                        print(f"📊 DEBUG: IGST Amount: {igst_amount} ({igst_percent}%)")
                        print(f"📊 DEBUG: Cess Amount: {cess_amount} ({cess_percent}%)")
                        print(f"📊 DEBUG: Tax Amount: {tax_amount}")
                        print(f"📊 DEBUG: Final Amount: {final_amount}")
                        
                        # Store line item data
                        line_items.append({
                            'material': material,
                            'material_name': material_names[i],
                            'quantity': quantity,
                            'mrp': mrp,
                            'discount': discount,
                            'basic_amount': basic_amount,
                            'cgst_amount': cgst_amount,
                            'sgst_amount': sgst_amount,
                            'igst_amount': igst_amount,
                            'cess_amount': cess_amount,
                            'tax_amount': tax_amount,
                            'final_amount': final_amount,
                            'cgst_rate': cgst_percent,
                            'sgst_rate': sgst_percent,
                            'igst_rate': igst_percent,
                            'cess_rate': cess_percent,
                        })
                        
                        # Update totals
                        total_taxable += basic_amount
                        total_cgst += cgst_amount
                        total_sgst += sgst_amount
                        total_igst += igst_amount
                        total_cess += cess_amount
                        total_amount += final_amount
                        
                    except Material.DoesNotExist:
                        messages.error(request, f'Material "{material_names[i]}" not found!')
                        return redirect('ajserp:addpurchaseorder')
                    except Exception as e:
                        messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                        return redirect('ajserp:addpurchaseorder')
            
            # Calculate grand total with round off
            grand_total = total_amount + round_off
            
            # Round totals to 2 decimal places
            total_taxable = round(total_taxable, 2)
            total_cgst = round(total_cgst, 2)
            total_sgst = round(total_sgst, 2)
            total_igst = round(total_igst, 2)
            total_cess = round(total_cess, 2)
            total_amount = round(total_amount, 2)
            grand_total = round(grand_total, 2)
            
            print(f"🎯 DEBUG: Final Totals:")
            print(f"🎯 DEBUG: Taxable Amount: {total_taxable}")
            print(f"🎯 DEBUG: CGST Total: {total_cgst}")
            print(f"🎯 DEBUG: SGST Total: {total_sgst}")
            print(f"🎯 DEBUG: IGST Total: {total_igst}")
            print(f"🎯 DEBUG: Cess Total: {total_cess}")
            print(f"🎯 DEBUG: Total Amount: {total_amount}")
            print(f"🎯 DEBUG: Round Off: {round_off}")
            print(f"🎯 DEBUG: Grand Total: {grand_total}")
            
            # Create Purchase Order
            purchase_order = PurchaseOrder.objects.create(
                vendor=vendor,
                warehouse=warehouse,
                date=date,
                valid_till=valid_till,
                ref_number=ref_number,
                description=description,
                terms_conditions=terms_conditions,
                billing_address1=billing_address1,
                billing_address2=billing_address2,
                billing_city=billing_city,
                billing_state=billing_state,
                billing_postal_code=billing_postal_code,
                taxable_amount=total_taxable,
                cgst=total_cgst,
                sgst=total_sgst,
                igst=total_igst,
                cess=total_cess,
                round_off=round_off,
                grand_total=grand_total,
                created_by=request.user
            )
            
            # Create Purchase Order Items
            for i, item_data in enumerate(line_items):
                PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order,
                    material=item_data['material'],
                    material_name=item_data['material_name'],
                    quantity=item_data['quantity'],
                    mrp=item_data['mrp'],
                    discount=item_data['discount'],
                    amount=item_data['basic_amount'],
                    sgst_rate=item_data['sgst_rate'],
                    cgst_rate=item_data['cgst_rate'],
                    igst_rate=item_data['igst_rate'],
                    cess_rate=item_data['cess_rate'],
                    sgst_amount=item_data['sgst_amount'],
                    cgst_amount=item_data['cgst_amount'],
                    igst_amount=item_data['igst_amount'],
                    cess_amount=item_data['cess_amount'],
                    sequence=i + 1
                )
            
            # Final verification with model method
            purchase_order.calculate_totals()
            
            messages.success(request, f'Purchase Order created successfully! Order Number: {purchase_order.order_number}')
            return redirect('ajserp:purchaseorder')
        
@login_required
def purchase_order_suggestions(request):
    """API for purchase order number suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 PURCHASE ORDER SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        purchase_orders = PurchaseOrder.objects.filter(
            order_number__icontains=query
        ).values('order_number', 'vendor__vendor_name')[:10]
        
        suggestions = []
        for order in purchase_orders:
            suggestions.append({
                'value': order['order_number'],
                'text': f"{order['order_number']} - {order['vendor__vendor_name']}"
            })
        
        print(f"✅ Found {len(suggestions)} purchase order suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in purchase_order_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    
@login_required
def vendor_search_po(request):
    """Unified vendor autocomplete API for Purchase Order"""
    q = request.GET.get("q", "").strip()
    print("🔍 Vendor Search Query:", q)

    if not q:
        return JsonResponse([], safe=False)

    try:
        vendors = Supplier.objects.filter(
            models.Q(vendor_name__icontains=q) |
            models.Q(vendor_code__icontains=q)
        )[:10]

        data = []

        for v in vendors:
            data.append({
                "vendor_name": v.vendor_name,
                "vendor_code": v.vendor_code,
                "billing_address1": v.billing_address1 or "",
                "billing_address2": v.billing_address2 or "",
                "billing_city": v.billing_city or "",
                "billing_state": v.billing_state or "",
                "billing_postal_code": v.billing_postal_code or "",
            })

        print("✅ Vendor results:", data)
        return JsonResponse(data, safe=False)

    except Exception as e:
        print("❌ Error:", e)
        return JsonResponse([], safe=False)


@login_required
def vendor_name_suggestions(request):
    query = request.GET.get('q', '').strip()
    print(f"🔍 VENDOR NAME SUGGESTIONS - Query: '{query}'")

    if not query:
        return JsonResponse([], safe=False)

    try:
        vendors = Supplier.objects.filter(
            vendor_name__icontains=query
        ).values('vendor_code', 'vendor_name')[:10]

        # FIX: Change format to match JavaScript expectation
        suggestions = [
            {
                'value': vendor['vendor_name'],   # Use vendor_name as value
                'text': f"{vendor['vendor_code']} - {vendor['vendor_name']}"  # Combined display
            }
            for vendor in vendors
        ]

        return JsonResponse(suggestions, safe=False)

    except Exception as e:
        print(f"❌ Error in vendor_name_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    


@login_required
def get_global_suggestions(request):
    """API for global purchase order search suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search purchase order numbers
        purchase_orders = PurchaseOrder.objects.filter(order_number__icontains=query)[:5]
        for order in purchase_orders:
            suggestions.append({
                'value': order.order_number,
                'text': f"Purchase Order: {order.order_number} - {order.vendor.vendor_name}"
            })
        
        # Search vendor names  
        vendors = Supplier.objects.filter(vendor_name__icontains=query)[:5]
        for vendor in vendors:
            suggestions.append({
                'value': vendor.vendor_name,
                'text': f"Vendor: {vendor.vendor_name}"
            })
        
        print(f"✅ Found {len(suggestions)} global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def purchaseorder(request):
    """Display list of all purchase orders"""
    purchase_orders = PurchaseOrder.objects.all().order_by('-date').prefetch_related('purchase_order_items')
    
    # Get filter parameters
    order_number = request.GET.get('order_number', '')
    vendor_name = request.GET.get('vendor_name', '')
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    q = request.GET.get('q', '')  # Global search parameter
    
    # Apply filters
    if order_number:
        purchase_orders = purchase_orders.filter(order_number__icontains=order_number)
    if vendor_name:
        purchase_orders = purchase_orders.filter(vendor__vendor_name__icontains=vendor_name)
    if status:
        purchase_orders = purchase_orders.filter(status=status)
    if from_date:
        purchase_orders = purchase_orders.filter(date__gte=from_date)
    if to_date:
        purchase_orders = purchase_orders.filter(date__lte=to_date)
        
    # Global search (search across multiple fields)
    if q:
        purchase_orders = purchase_orders.filter(
            models.Q(order_number__icontains=q) |
            models.Q(vendor__vendor_name__icontains=q) |
            models.Q(billing_city__icontains=q) |
            models.Q(ref_number__icontains=q)
        )
        
    # Pagination - Show 10 purchase orders per page
    paginator = Paginator(purchase_orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "ajserpadmin/purchaseorder.html", {
        'purchase_orders': page_obj,
        'page_obj': page_obj,
    })

@login_required
def edit_purchase_order(request, order_id):
    """Edit an existing purchase order"""
    purchase_order = get_object_or_404(PurchaseOrder, id=order_id)
    
    if request.method == 'POST':
        try:
            print(f"🔧 EDITING PURCHASE ORDER {purchase_order.order_number}")
            print("📝 POST data:", dict(request.POST))
            
            # Get basic info
            vendor_id = request.POST.get('vendor')
            date = request.POST.get('date')
            valid_till = request.POST.get('valid_till')
            ref_number = request.POST.get('ref_number', '')
            description = request.POST.get('description', '')
            terms_conditions = request.POST.get('terms_conditions', '')
            
            # Get billing address
            billing_address1 = request.POST.get('billing_address1', '')
            billing_address2 = request.POST.get('billing_address2', '')
            billing_city = request.POST.get('billing_city', '')
            billing_state = request.POST.get('billing_state', '')
            billing_postal_code = request.POST.get('billing_postal_code', '')
            
            # Get round off
            round_off = float(request.POST.get('round_off', 0))
            
            # Get vendor
            vendor = get_object_or_404(Supplier, id=vendor_id)
            
            # Update purchase order fields
            purchase_order.vendor = vendor
            purchase_order.date = date
            purchase_order.valid_till = valid_till
            purchase_order.ref_number = ref_number
            purchase_order.description = description
            purchase_order.terms_conditions = terms_conditions
            purchase_order.billing_address1 = billing_address1
            purchase_order.billing_address2 = billing_address2
            purchase_order.billing_city = billing_city
            purchase_order.billing_state = billing_state
            purchase_order.billing_postal_code = billing_postal_code
            purchase_order.round_off = round_off
            
            # Handle line items if provided
            material_names = request.POST.getlist('material_name[]')
            quantities = request.POST.getlist('quantity[]')
            mrps = request.POST.getlist('mrp[]')
            discounts = request.POST.getlist('discount[]')
            hsn_codes = request.POST.getlist('hsn_code[]')
            
            if material_names and material_names[0]:  # If items are provided
                # Delete existing items
                purchase_order.purchase_order_items.all().delete()
                
                # Create new items
                for i in range(len(material_names)):
                    if material_names[i]:
                        try:
                            material = Material.objects.get(material_name=material_names[i])
                            
                            quantity = float(quantities[i]) if quantities[i] else 0
                            mrp = float(mrps[i]) if mrps[i] else 0
                            discount = float(discounts[i]) if discounts[i] else 0
                            
                            # Get tax rates
                            try:
                                hsn_obj = HSNCode.objects.get(hsn_code=hsn_codes[i])
                                tax_rate = Taxes.objects.get(hsn_code=hsn_obj)
                                cgst_percent = float(tax_rate.cgst)
                                sgst_percent = float(tax_rate.sgst)
                                igst_percent = float(tax_rate.igst)
                                cess_percent = float(tax_rate.cess)
                            except (HSNCode.DoesNotExist, Taxes.DoesNotExist):
                                # Use default tax rates if not found
                                cgst_percent = 9
                                sgst_percent = 9
                                igst_percent = 18
                                cess_percent = 0
                            
                            # Calculate amounts
                            after_discount = mrp - discount
                            basic_amount = quantity * after_discount
                            cgst_amount = (basic_amount * cgst_percent) / 100
                            sgst_amount = (basic_amount * sgst_percent) / 100
                            igst_amount = (basic_amount * igst_percent) / 100
                            cess_amount = (basic_amount * cess_percent) / 100
                            tax_amount = cgst_amount + sgst_amount + igst_amount + cess_amount
                            final_amount = basic_amount + tax_amount
                            
                            # Create purchase order item
                            PurchaseOrderItem.objects.create(
                                purchase_order=purchase_order,
                                material=material,
                                material_name=material_names[i],
                                quantity=quantity,
                                mrp=mrp,
                                discount=discount,
                                amount=round(basic_amount, 2),
                                sgst_rate=sgst_percent,
                                cgst_rate=cgst_percent,
                                igst_rate=igst_percent,
                                cess_rate=cess_percent,
                                sgst_amount=round(sgst_amount, 2),
                                cgst_amount=round(cgst_amount, 2),
                                igst_amount=round(igst_amount, 2),
                                cess_amount=round(cess_amount, 2),
                                sequence=i + 1
                            )
                            
                        except Material.DoesNotExist:
                            messages.error(request, f'Material "{material_names[i]}" not found!')
                            return redirect('ajserp:purchaseorder')
                        except Exception as e:
                            messages.error(request, f'Error processing material {material_names[i]}: {str(e)}')
                            return redirect('ajserp:purchaseorder')
            
            # Recalculate totals
            purchase_order.calculate_totals()
            purchase_order.save()
            
            messages.success(request, f'Purchase Order {purchase_order.order_number} updated successfully!')
            return redirect('ajserp:purchaseorder')
            
        except Exception as e:
            print(f"❌ Error updating purchase order: {str(e)}")
            messages.error(request, f'Error updating purchase order: {str(e)}')
            return redirect('ajserp:purchaseorder')
    
    # For GET request, redirect to purchase orders list
    return redirect('ajserp:purchaseorder')

@login_required
def delete_purchase_order(request, order_id):
    """Delete a purchase order"""
    if request.method == 'POST':
        try:
            purchase_order = get_object_or_404(PurchaseOrder, id=order_id)
            order_number = purchase_order.order_number
            purchase_order.delete()
            messages.success(request, f'Purchase Order {order_number} deleted successfully!')
        except PurchaseOrder.DoesNotExist:
            messages.error(request, 'Purchase Order not found!')
        except Exception as e:
            messages.error(request, f'Error deleting purchase order: {str(e)}')
    
    return redirect('ajserp:purchaseorder')

# API Views for Purchase Order
@login_required
def get_purchase_order_suggestions(request):
    """Get purchase order number suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 PURCHASE ORDER SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        purchase_orders = PurchaseOrder.objects.filter(
            order_number__icontains=query
        ).values('order_number', 'vendor__vendor_name')[:10]
        
        suggestions = []
        for order in purchase_orders:
            suggestions.append({
                'value': order['order_number'],
                'text': f"{order['order_number']} - {order['vendor__vendor_name']}"
            })
        
        print(f"✅ Found {len(suggestions)} purchase order suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_purchase_order_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_purchase_order_global_suggestions(request):
    """Get global search suggestions for purchase orders"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 PURCHASE ORDER GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search purchase order numbers
        purchase_orders = PurchaseOrder.objects.filter(order_number__icontains=query)[:5]
        for order in purchase_orders:
            suggestions.append({
                'value': order.order_number,
                'text': f"Purchase Order: {order.order_number} - {order.vendor.vendor_name}"
            })
        
        # Search vendor names  
        vendors = Supplier.objects.filter(vendor_name__icontains=query)[:5]
        for vendor in vendors:
            suggestions.append({
                'value': vendor.vendor_name,
                'text': f"Vendor: {vendor.vendor_name}"
            })
        
        print(f"✅ Found {len(suggestions)} purchase order global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_purchase_order_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_vendor_details_po(request):
    vendor_code = request.GET.get("vendor_code", "").strip()

    if not vendor_code:
        return JsonResponse({"success": False, "message": "Vendor code missing"})

    try:
        vendor = Supplier.objects.get(vendor_code=vendor_code)

        return JsonResponse({
            "success": True,
            "vendor_code": vendor.vendor_code,
            "vendor_name": vendor.vendor_name,
            "billing_address1": vendor.billing_address1 or "",
            "billing_address2": vendor.billing_address2 or "",
            "billing_city": vendor.billing_city or "",
            "billing_state": vendor.billing_state or "",
            "billing_postal_code": vendor.billing_postal_code or "",
        })

    except Supplier.DoesNotExist:
        return JsonResponse({"success": False, "message": "Vendor not found"})

@login_required
def claimrequest(request):
    """Main claim request list page (render full HTML page)."""
    claims = ClaimRequest.objects.select_related('requested_by', 'approved_by').prefetch_related('items').all().order_by('-created_at')

    # Filter parameters
    document_no = request.GET.get('document_no', '').strip()
    requested_by = request.GET.get('requested_by', '').strip()
    status = request.GET.get('status', '').strip()
    from_date = request.GET.get('from_date', '').strip()
    to_date = request.GET.get('to_date', '').strip()

    if document_no:
        claims = claims.filter(document_number__icontains=document_no)
    if requested_by:
        claims = claims.filter(requested_by__username__icontains=requested_by)
    if status:
        claims = claims.filter(status=status)
    if from_date:
        claims = claims.filter(created_at__date__gte=from_date)
    if to_date:
        claims = claims.filter(created_at__date__lte=to_date)

    # Pagination for page view (10 per page)
    paginator = Paginator(claims, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'claims': page_obj,
        'search_params': {
            'document_no': document_no,
            'requested_by': requested_by,
            'status': status,
            'from_date': from_date,
            'to_date': to_date,
        }
    }
    return render(request, 'ajserpadmin/claimrequest.html', context)


# -------------------------
# Page: add/edit claim
# -------------------------
@login_required
def addclaimrequest(request):
    """Add or edit claim request (form view)."""
    claim_id = request.GET.get('edit')
    claim = None
    items = []

    # If editing, load existing claim
    if claim_id:
        try:
            claim = ClaimRequest.objects.get(id=claim_id)
            items = claim.items.all()
        except ClaimRequest.DoesNotExist:
            messages.error(request, 'Claim request not found!')
            return redirect('ajserp:claimrequest')

    if request.method == 'POST':
        try:
            # Read form fields (strings). Convert numeric fields as needed.
            previous_advance = request.POST.get('previous_advance') or 0
            pending_claim = request.POST.get('pending_claim') or 0
            payment_reference = request.POST.get('payment_reference', '').strip()
            remarks = request.POST.get('remarks', '').strip()

            # If editing, update fields
            if claim_id and claim:
                claim.previous_advance = previous_advance
                claim.pending_claim = pending_claim
                claim.payment_reference = payment_reference
                claim.remarks = remarks
                claim.save()

                # Remove existing items; will recreate from POST data
                claim.items.all().delete()
                action_message = 'updated'
            else:
                # Create new claim (requested_by = current user)
                claim = ClaimRequest.objects.create(
                    requested_by=request.user,
                    previous_advance=previous_advance,
                    pending_claim=pending_claim,
                    payment_reference=payment_reference,
                    remarks=remarks
                )
                action_message = 'created'

            # Process items posted as items[0][type], items[1][type], ...
            i = 0
            item_count = 0
            while True:
                type_key = f'items[{i}][type]'
                if type_key not in request.POST:
                    break

                type_val = request.POST.get(type_key)
                uom_val = request.POST.get(f'items[{i}][uom]')
                quantity_val = request.POST.get(f'items[{i}][quantity]')
                amount_val = request.POST.get(f'items[{i}][amount]')
                remarks_val = request.POST.get(f'items[{i}][remarks]', '')

                if type_val and uom_val and quantity_val and amount_val:
                    ClaimRequestItem.objects.create(
                        claim_request=claim,
                        type=type_val,
                        uom=uom_val,
                        quantity=quantity_val,
                        amount=amount_val,
                        remarks=remarks_val
                    )
                    item_count += 1

                i += 1

            if item_count > 0:
                messages.success(request, f'Claim request {claim.document_number} {action_message} successfully with {item_count} items!')
                return redirect('ajserp:claimrequest')
            else:
                # If no items provided, remove newly created claim (if it was new)
                messages.error(request, 'Please add at least one claim item.')
                if not claim_id and claim:
                    claim.delete()

        except Exception as e:
            messages.error(request, f'Error saving claim request: {str(e)}')

    # GET or error -> render form
    context = {
        'claim': claim,
        'items': items,
        'is_edit': bool(claim_id),
    }
    return render(request, 'ajserpadmin/addclaimrequest.html', context)


# -------------------------------------------------------
# API: list/create claims (used by JS)
# -------------------------------------------------------
@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def claim_requests_api(request):
    """API endpoint to list (GET) or create (POST) claim requests via JSON."""
    if request.method == 'GET':
        claims = ClaimRequest.objects.select_related('requested_by', 'approved_by').prefetch_related('items').all().order_by('-created_at')

        claims_data = []
        for claim in claims:
            total_quantity = sum((item.quantity or 0) for item in claim.items.all())
            total_amount = sum((item.amount or 0) for item in claim.items.all())
            claims_data.append({
                'id': claim.id,
                'document_number': claim.document_number,
                'date': claim.date.strftime('%Y-%m-%d') if claim.date else '',
                'requested_by': claim.requested_by.username if claim.requested_by else '',
                'quantity': float(total_quantity),
                'amount': float(total_amount),
                'remarks': claim.remarks,
                'status': claim.status,
                'status_display': claim.get_status_display() if hasattr(claim, 'get_status_display') else claim.status,
                'created_at': claim.created_at.strftime('%Y-%m-%d %H:%M:%S') if claim.created_at else ''
            })

        return JsonResponse({'claims': claims_data})

    # POST -> create via JSON
    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    try:
        claim = ClaimRequest.objects.create(
            requested_by=request.user,
            previous_advance=data.get('previous_advance', 0),
            pending_claim=data.get('pending_claim', 0),
            payment_reference=data.get('payment_reference', ''),
            remarks=data.get('remarks', '')
        )

        for item_data in data.get('items', []):
            ClaimRequestItem.objects.create(
                claim_request=claim,
                type=item_data.get('type'),
                uom=item_data.get('uom'),
                quantity=item_data.get('quantity'),
                amount=item_data.get('amount'),
                remarks=item_data.get('remarks', '')
            )

        response_data = {'id': claim.id, 'document_number': claim.document_number, 'message': 'Claim request created successfully!'}
        return JsonResponse(response_data, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# -------------------------------------------------------
# API: detail / update / delete (claim_id)
# -------------------------------------------------------
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
@login_required
def claim_request_detail_api(request, claim_id):
    claim = get_object_or_404(ClaimRequest, id=claim_id)

    if request.method == 'GET':
        claim_data = {
            'id': claim.id,
            'document_number': claim.document_number,
            'date': claim.date.strftime('%Y-%m-%d') if claim.date else '',
            'requested_by': claim.requested_by.username if claim.requested_by else '',
            'previous_advance': float(claim.previous_advance or 0),
            'pending_claim': float(claim.pending_claim or 0),
            'payment_reference': claim.payment_reference,
            'remarks': claim.remarks,
            'status': claim.status,
            'status_display': claim.get_status_display() if hasattr(claim, 'get_status_display') else claim.status,
            'items': []
        }

        for item in claim.items.all():
            claim_data['items'].append({
                'type': item.type,
                'uom': item.uom,
                'quantity': float(item.quantity or 0),
                'amount': float(item.amount or 0),
                'remarks': item.remarks or ''
            })

        return JsonResponse(claim_data)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8') or '{}')
            claim.previous_advance = data.get('previous_advance', claim.previous_advance)
            claim.pending_claim = data.get('pending_claim', claim.pending_claim)
            claim.payment_reference = data.get('payment_reference', claim.payment_reference)
            claim.remarks = data.get('remarks', claim.remarks)
            claim.save()
            return JsonResponse({'message': 'Claim request updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # DELETE
    try:
        document_number = claim.document_number
        claim.delete()
        return JsonResponse({'message': f'Claim request {document_number} deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# -------------------------------------------------------
# Approval APIs (approve / reject / query)
# -------------------------------------------------------
@csrf_exempt
@require_http_methods(["POST"])
@login_required
def claim_approval_api(request, claim_id):
    """Generic approval action handler (approve / reject / query)."""
    claim = get_object_or_404(ClaimRequest, id=claim_id)
    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
        action = data.get('action')
        remarks = data.get('remarks', '')

        if action == 'approve':
            claim.status = 'approved'
            claim.approved_by = request.user
            claim.manager_approved_at = timezone.now()
            claim.manager_action_at = timezone.now()
            claim.manager_action_type = 'approved'
        elif action == 'reject':
            claim.status = 'rejected'
            claim.approved_by = request.user
            claim.manager_rejected_at = timezone.now()
            claim.manager_action_at = timezone.now()
            claim.manager_action_type = 'rejected'
        elif action == 'query':
            claim.status = 'query_raised'
            claim.manager_query_raised_at = timezone.now()
            claim.manager_action_at = timezone.now()
            claim.manager_action_type = 'query_raised'
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        claim.manager_action_remarks = remarks
        claim.save()

        return JsonResponse({
            'message': f'Claim {action}d successfully',
            'status': claim.status,
            'status_display': claim.get_status_display() if hasattr(claim, 'get_status_display') else claim.status
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# -------------------------
# Delete via POST (form)
# -------------------------
@login_required
def delete_claim_request(request, claim_id):
    """Handle claim deletion via POST (form)."""
    if request.method == 'POST':
        try:
            claim = get_object_or_404(ClaimRequest, id=claim_id)
            document_number = claim.document_number
            claim.delete()
            messages.success(request, f'Claim request {document_number} deleted successfully!')
        except ClaimRequest.DoesNotExist:
            messages.error(request, 'Claim request not found!')
        except Exception as e:
            messages.error(request, f'Error deleting claim request: {str(e)}')

    return redirect('ajserp:claimrequest')


# -------------------------
# Modal details (AJAX)
# -------------------------
@login_required
def get_claim_details(request, claim_id):
    """Return JSON with claim details for the approval modal."""
    try:
        claim = ClaimRequest.objects.select_related('requested_by', 'approved_by').prefetch_related('items').get(id=claim_id)
    except ClaimRequest.DoesNotExist:
        return JsonResponse({'error': 'Claim not found'}, status=404)

    claim_data = {
        'id': claim.id,
        'document_number': claim.document_number,
        'date': claim.created_at.strftime('%Y-%m-%d') if claim.created_at else '',
        'requested_by': claim.requested_by.get_full_name() or claim.requested_by.username if claim.requested_by else '',
        'previous_advance': float(claim.previous_advance or 0),
        'pending_claim': float(claim.pending_claim or 0),
        'payment_reference': claim.payment_reference,
        'remarks': claim.remarks,
        'status': claim.status,
        'approved_by': claim.approved_by.get_full_name() if claim.approved_by else '',
        'approval_remarks': claim.approval_remarks or '',
        'items': []
    }

    for item in claim.items.all():
        claim_data['items'].append({
            'type': item.type,
            'uom': item.uom,
            'quantity': float(item.quantity or 0),
            'amount': float(item.amount or 0),
            'remarks': item.remarks or ''
        })

    return JsonResponse(claim_data)


# -------------------------
# Claim approval detail page (form)
# -------------------------
@login_required
def claim_approval_page(request, claim_id):
    """Render claim approval detail page and allow repeated approvals."""
    try:
        claim = ClaimRequest.objects.select_related('requested_by', 'approved_by').prefetch_related('items').get(id=claim_id)
    except ClaimRequest.DoesNotExist:
        messages.error(request, 'Claim request not found!')
        return redirect('ajserp:claimrequest')

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')

        if action == 'approve':
            claim.status = 'approved'
            claim.approved_by = request.user
            claim.manager_approved_at = timezone.now()
            claim.manager_action_at = timezone.now()
            claim.manager_action_type = 'approved'
            messages.success(request, f'Claim {claim.document_number} approved successfully!')
        elif action == 'reject':
            claim.status = 'rejected'
            claim.approved_by = request.user
            claim.manager_rejected_at = timezone.now()
            claim.manager_action_at = timezone.now()
            claim.manager_action_type = 'rejected'
            messages.success(request, f'Claim {claim.document_number} rejected!')
        elif action == 'query':
            claim.status = 'query_raised'
            claim.manager_query_raised_at = timezone.now()
            claim.manager_action_at = timezone.now()
            claim.manager_action_type = 'query_raised'
            messages.success(request, f'Query raised for claim {claim.document_number}!')

        claim.manager_action_remarks = remarks
        claim.save()
        return redirect('ajserp:claimrequest')

    return render(request, 'ajserpadmin/claim_approval_detail.html', {'claim': claim})


# -------------------------
# Claim approval listing (page)
# -------------------------
@login_required
def claimapproval(request):
    """Claim approval page - show all claims with optional filters."""
    claims = ClaimRequest.objects.select_related('requested_by', 'approved_by').prefetch_related('items').all().order_by('-created_at')

    document_no = request.GET.get('document_no', '').strip()
    requested_by = request.GET.get('requested_by', '').strip()
    status = request.GET.get('status', '').strip()

    if document_no:
        claims = claims.filter(document_number__icontains=document_no)
    if requested_by:
        claims = claims.filter(requested_by__username__icontains=requested_by)
    if status:
        claims = claims.filter(status=status)

    context = {'claims': claims, 'current_status': status}
    return render(request, 'ajserpadmin/claimapproval.html', context)


# -------------------------
# claim_request_list (AJAX paginated view)
# -------------------------
@login_required
def claim_request_list(request):
    """AJAX-friendly paginated list endpoint (returns JSON if requested)."""
    claims = ClaimRequest.objects.select_related('requested_by').prefetch_related('items').all().order_by('-employee_submitted_at')

    document_no = request.GET.get('document_no', '').strip()
    requested_by = request.GET.get('requested_by', '').strip()
    status = request.GET.get('status', '').strip()
    from_date = request.GET.get('from_date', '').strip()
    to_date = request.GET.get('to_date', '').strip()
    global_search = request.GET.get('global_search', '').strip()

    if document_no:
        claims = claims.filter(document_number__icontains=document_no)
    if requested_by:
        claims = claims.filter(requested_by__username__icontains=requested_by)
    if status:
        claims = claims.filter(status=status)
    if from_date:
        claims = claims.filter(created_at__date__gte=from_date)
    if to_date:
        claims = claims.filter(created_at__date__lte=to_date)
    if global_search:
        claims = claims.filter(
            Q(document_number__icontains=global_search) |
            Q(requested_by__username__icontains=global_search) |
            Q(remarks__icontains=global_search) |
            Q(items__type__icontains=global_search) |
            Q(status__icontains=global_search)
        ).distinct()

    paginator = Paginator(claims, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # AJAX request returns JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        claims_data = []
        for claim in page_obj:
            claims_data.append({
                'id': claim.id,
                'document_number': claim.document_number,
                'requested_by': claim.requested_by.username if claim.requested_by else '',
                'status': claim.status,
                'remarks': claim.remarks or '-',
                'employee_submitted_at': claim.employee_submitted_at.strftime('%b %d, %Y %H:%M:%S') if claim.employee_submitted_at else '',
                'manager_action_at': claim.manager_action_at.strftime('%b %d, %Y %H:%M:%S') if claim.manager_action_at else None,
                'manager_action_type': claim.manager_action_type,
                'items': [{
                    'type': item.type,
                    'uom': item.uom,
                    'quantity': str(item.quantity),
                    'amount': str(item.amount)
                } for item in claim.items.all()]
            })
        return JsonResponse({
            'claims': claims_data,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        })

    # Regular page render
    context = {
        'claims': page_obj,
        'search_params': {
            'document_no': document_no,
            'requested_by': requested_by,
            'status': status,
            'from_date': from_date,
            'to_date': to_date,
            'global_search': global_search,
        }
    }
    return render(request, 'ajserpadmin/claimrequest.html', context)


# -------------------------
# search_claims (API)
# -------------------------
@login_required
def search_claims(request):
    """Dedicated API endpoint used by JS to fetch filtered claims (returns JSON)."""
    if request.method != 'GET':
        return HttpResponseBadRequest('Only GET allowed')

    claims = ClaimRequest.objects.select_related('requested_by').prefetch_related('items').all().order_by('-employee_submitted_at')

    document_no = request.GET.get('document_no', '').strip()
    requested_by = request.GET.get('requested_by', '').strip()
    status = request.GET.get('status', '').strip()
    from_date = request.GET.get('from_date', '').strip()
    to_date = request.GET.get('to_date', '').strip()
    global_search = request.GET.get('global_search', '').strip()

    if document_no:
        claims = claims.filter(document_number__icontains=document_no)
    if requested_by:
        claims = claims.filter(requested_by__username__icontains=requested_by)
    if status:
        claims = claims.filter(status=status)
    if from_date:
        claims = claims.filter(created_at__date__gte=from_date)
    if to_date:
        claims = claims.filter(created_at__date__lte=to_date)
    if global_search:
        claims = claims.filter(
            Q(document_number__icontains=global_search) |
            Q(requested_by__username__icontains=global_search) |
            Q(remarks__icontains=global_search) |
            Q(items__type__icontains=global_search) |
            Q(status__icontains=global_search)
        ).distinct()

    claims_data = []
    for claim in claims:
        claims_data.append({
            'id': claim.id,
            'document_number': claim.document_number,
            'requested_by': claim.requested_by.username if claim.requested_by else '',
            'status': claim.status,
            'remarks': claim.remarks or '-',
            'employee_submitted_at': claim.employee_submitted_at.strftime('%b %d, %Y %H:%M:%S') if claim.employee_submitted_at else '',
            'manager_action_at': claim.manager_action_at.strftime('%b %d, %Y %H:%M:%S') if claim.manager_action_at else None,
            'manager_action_type': claim.manager_action_type,
            'items': [{
                'type': item.type,
                'uom': item.uom,
                'quantity': str(item.quantity),
                'amount': str(item.amount),
            } for item in claim.items.all()]
        })

    return JsonResponse({'claims': claims_data})


# -------------------------
# Autocomplete endpoints (document numbers, requested_by)
# -------------------------
@login_required
def get_claim_document_numbers(request):
    """API to get document numbers for autocomplete"""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'document_numbers': []})

    try:
        document_numbers = ClaimRequest.objects.filter(
            document_number__icontains=query
        ).values_list('document_number', flat=True).distinct()[:10]

        results = list(document_numbers)
        return JsonResponse({'document_numbers': results})
    except Exception:
        return JsonResponse({'document_numbers': []})


@login_required
def get_claim_requested_by(request):
    """API to get requested_by usernames for autocomplete"""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'usernames': []})

    try:
        usernames = ClaimRequest.objects.filter(
            requested_by__username__icontains=query
        ).values_list('requested_by__username', flat=True).distinct()[:10]

        results = list(usernames)
        return JsonResponse({'usernames': results})
    except Exception:
        return JsonResponse({'usernames': []})

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def claim_approval_api(request, claim_id):
    """API endpoint for claim approval actions"""
    claim = get_object_or_404(ClaimRequest, id=claim_id)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')
        remarks = data.get('remarks', '')
        
        if action == 'approve':
            claim.status = 'approved'
            claim.approved_by = request.user
        elif action == 'reject':
            claim.status = 'rejected'
        elif action == 'query':
            claim.status = 'query_raised'
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
        claim.remarks = remarks
        claim.save()
        
        return JsonResponse({
            'message': f'Claim {action}d successfully',
            'status': claim.status,
            'status_display': claim.get_status_display()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def delete_claim_request(request, claim_id):
    """Handle claim deletion via POST"""
    if request.method == 'POST':
        try:
            claim = get_object_or_404(ClaimRequest, id=claim_id)
            document_number = claim.document_number
            claim.delete()
            messages.success(request, f'Claim request {document_number} deleted successfully!')
        except ClaimRequest.DoesNotExist:
            messages.error(request, 'Claim request not found!')
        except Exception as e:
            messages.error(request, f'Error deleting claim request: {str(e)}')
    
    return redirect('ajserp:claimrequest')

@login_required
def add_claim_request(request):
    claim_id = request.GET.get('edit')
    if claim_id:
        # Edit existing claim
        claim = get_object_or_404(claimrequest, id=claim_id)
        # Your edit logic here
    else:
        # Add new claim
        # Your add logic here
        pass  # Added this line to fix the indentation error
    
    return render(request, 'addclaimrequest.html')

@login_required
def edit_claim_request(request, claim_id):
    """Edit an existing claim request"""
    try:
        claim = get_object_or_404(ClaimRequest, id=claim_id)
        
        if request.method == 'POST':
            # Handle form submission for editing
            claim.previous_advance = request.POST.get('previous_advance', 0) or 0
            claim.pending_claim = request.POST.get('pending_claim', 0) or 0
            claim.payment_reference = request.POST.get('payment_reference', '')
            claim.remarks = request.POST.get('remarks', '')
            claim.save()
            
            # Update claim items
            # Clear existing items
            claim.items.all().delete()
            
            # Add new items
            i = 0
            while True:
                type_key = f'items[{i}][type]'
                if type_key not in request.POST:
                    break
                
                type_val = request.POST.get(type_key)
                uom_val = request.POST.get(f'items[{i}][uom]')
                quantity_val = request.POST.get(f'items[{i}][quantity]')
                amount_val = request.POST.get(f'items[{i}][amount]')
                remarks_val = request.POST.get(f'items[{i}][remarks]', '')
                
                if type_val and uom_val and quantity_val and amount_val:
                    ClaimRequestItem.objects.create(
                        claim_request=claim,
                        type=type_val,
                        uom=uom_val,
                        quantity=quantity_val,
                        amount=amount_val,
                        remarks=remarks_val
                    )
                
                i += 1
            
            messages.success(request, f'Claim request {claim.document_number} updated successfully!')
            return redirect('ajserp:claimrequest')
        
        # GET request - render edit form with existing data
        return render(request, 'ajserpadmin/edit_claim_request.html', {
            'claim': claim,
            'items': claim.items.all()
        })
        
    except Exception as e:
        messages.error(request, f'Error editing claim request: {str(e)}')
        return redirect('ajserp:claimrequest')

@login_required
def get_claim_details(request, claim_id):
    """Get claim details for approval modal"""
    try:
        claim = ClaimRequest.objects.select_related('requested_by').prefetch_related('items').get(id=claim_id)
        
        claim_data = {
            'id': claim.id,
            'document_number': claim.document_number,
            'date': claim.created_at.strftime('%Y-%m-%d'),
            'requested_by': claim.requested_by.get_full_name() or claim.requested_by.username,
            'previous_advance': float(claim.previous_advance),
            'pending_claim': float(claim.pending_claim),
            'payment_reference': claim.payment_reference,
            'remarks': claim.remarks,
            'status': claim.status,
            'approved_by': claim.approved_by.get_full_name() if claim.approved_by else '',
            'approval_remarks': claim.approval_remarks or '',
            'items': []
        }
        
        # Add claim items
        for item in claim.items.all():
            claim_data['items'].append({
                'type': item.type,
                'uom': item.uom,
                'quantity': float(item.quantity),
                'amount': float(item.amount),
                'remarks': item.remarks or ''
            })
        
        return JsonResponse(claim_data)
        
    except ClaimRequest.DoesNotExist:
        return JsonResponse({'error': 'Claim not found'}, status=404)

@login_required
def approve_claim(request, claim_id):
    """Approve a claim request - can be called multiple times"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            claim = ClaimRequest.objects.get(id=claim_id)
            
            # Update status and timestamps
            claim.status = 'approved'
            claim.approved_by = request.user
            claim.manager_approved_at = timezone.now()
            claim.manager_action_at = timezone.now()  # Latest action timestamp
            claim.manager_action_type = 'approved'
            claim.manager_action_remarks = data.get('remarks', '')
            claim.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Claim {claim.document_number} approved successfully!',
                'status': claim.status,
                'manager_action_time': claim.manager_action_at.strftime('%Y-%m-%d %H:%M:%S'),
                'manager_action_type': claim.manager_action_type
            })
            
        except ClaimRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Claim not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@login_required
def reject_claim(request, claim_id):
    """Reject a claim request - can be called multiple times"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            claim = ClaimRequest.objects.get(id=claim_id)
            
            claim.status = 'rejected'
            claim.approved_by = request.user
            claim.manager_rejected_at = timezone.now()
            claim.manager_action_at = timezone.now()  # Latest action timestamp
            claim.manager_action_type = 'rejected'
            claim.manager_action_remarks = data.get('remarks', '')
            claim.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Claim {claim.document_number} rejected!',
                'status': claim.status,
                'manager_action_time': claim.manager_action_at.strftime('%Y-%m-%d %H:%M:%S'),
                'manager_action_type': claim.manager_action_type
            })
            
        except ClaimRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Claim not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@login_required
def query_claim(request, claim_id):
    """Raise query on a claim request - can be called multiple times"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            claim = ClaimRequest.objects.get(id=claim_id)
            
            claim.status = 'query_raised'
            claim.manager_query_raised_at = timezone.now()
            claim.manager_action_at = timezone.now()  # Latest action timestamp
            claim.manager_action_type = 'query_raised'
            claim.manager_action_remarks = data.get('remarks', '')
            claim.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Query raised for claim {claim.document_number}!',
                'status': claim.status,
                'manager_action_time': claim.manager_action_at.strftime('%Y-%m-%d %H:%M:%S'),
                'manager_action_type': claim.manager_action_type
            })
            
        except ClaimRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Claim not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@login_required
def save_claim_approval(request, claim_id):
    """Save approval data without changing status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            claim = ClaimRequest.objects.get(id=claim_id)
            
            # Update approval data
            claim.previous_advance = data.get('previous_advance', claim.previous_advance)
            claim.pending_claim = data.get('pending_claim', claim.pending_claim)
            claim.payment_reference = data.get('payment_reference', claim.payment_reference)
            claim.approval_remarks = data.get('approval_remarks', claim.approval_remarks)
            claim.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Claim {claim.document_number} data saved successfully!'
            })
            
        except ClaimRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Claim not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)   

@login_required
def claim_approval_page(request, claim_id):
    """Claim approval page view using existing template - ALLOW RE-APPROVALS"""
    try:
        claim = ClaimRequest.objects.select_related('requested_by', 'approved_by').prefetch_related('items').get(id=claim_id)
        
        if request.method == 'POST':
            # Handle approval actions - ALLOW MULTIPLE TIMES
            action = request.POST.get('action')
            remarks = request.POST.get('remarks', '')
            
            if action == 'approve':
                claim.status = 'approved'
                claim.approved_by = request.user
                claim.manager_approved_at = timezone.now()
                claim.manager_action_at = timezone.now()
                claim.manager_action_type = 'approved'
                messages.success(request, f'Claim {claim.document_number} approved successfully!')
            elif action == 'reject':
                claim.status = 'rejected'
                claim.approved_by = request.user
                claim.manager_rejected_at = timezone.now()
                claim.manager_action_at = timezone.now()
                claim.manager_action_type = 'rejected'
                messages.success(request, f'Claim {claim.document_number} rejected!')
            elif action == 'query':
                claim.status = 'query_raised'
                claim.manager_query_raised_at = timezone.now()
                claim.manager_action_at = timezone.now()
                claim.manager_action_type = 'query_raised'
                messages.success(request, f'Query raised for claim {claim.document_number}!')
            
            claim.manager_action_remarks = remarks
            claim.save()
            return redirect('ajserp:claimrequest')
        
        context = {
            'claim': claim,
        }
        return render(request, 'ajserpadmin/claim_approval_detail.html', context)
        
    except ClaimRequest.DoesNotExist:
        messages.error(request, 'Claim request not found!')
        return redirect('ajserp:claimrequest')         

@login_required
def claimapproval(request):
    """Claim approval page - show all claims for approval with filters"""
    print("🔄 Claim Approval view called!")  # Debug line
    
    # Get all claims for approval
    claims = ClaimRequest.objects.select_related('requested_by', 'approved_by').prefetch_related('items').all().order_by('-created_at')
    
    # Filter functionality for approval page
    document_no = request.GET.get('document_no')
    requested_by = request.GET.get('requested_by')
    status = request.GET.get('status', '')  # No default - show all

    if document_no:
        claims = claims.filter(document_number__icontains=document_no)
    if requested_by:
        claims = claims.filter(requested_by_username_icontains=requested_by)
    if status:
        claims = claims.filter(status=status)
    
    context = {
        'claims': claims,
        'current_status': status
    }
    return render(request, 'ajserpadmin/claimapproval.html', context)

@login_required
def claim_request_list(request):
    # Get all claims for initial load
    claims = ClaimRequest.objects.select_related('requested_by').prefetch_related('items').all().order_by('-employee_submitted_at')
    
    # Apply filters if provided
    document_no = request.GET.get('document_no', '')
    requested_by = request.GET.get('requested_by', '')
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    global_search = request.GET.get('global_search', '')
    
    if document_no:
        claims = claims.filter(document_number__icontains=document_no)
    
    if requested_by:
        claims = claims.filter(requested_by_username_icontains=requested_by)
    
    if status:
        claims = claims.filter(status=status)
    
    if from_date:
        claims = claims.filter(created_at__gte=from_date)
    
    if to_date:
        claims = claims.filter(created_at__lte=to_date)
    
    if global_search:
        claims = claims.filter(
            Q(document_number__icontains=global_search) |
            Q(requested_by_username_icontains=global_search) |
            Q(remarks__icontains=global_search) |
            Q(items_type_icontains=global_search) |
            Q(status__icontains=global_search)
        ).distinct()
    
    # Pagination
    paginator = Paginator(claims, 10)  
    #Show 10 claims per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'claims': page_obj,
        'search_params': {
            'document_no': document_no,
            'requested_by': requested_by,
            'status': status,
            'from_date': from_date,
            'to_date': to_date,
            'global_search': global_search,
        }
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX request - return JSON for dynamic updates
        claims_data = []
        for claim in page_obj:
            claim_data = {
                'id': claim.id,
                'document_number': claim.document_number,
                'requested_by': claim.requested_by.username,
                'status': claim.status,
                'remarks': claim.remarks or '-',
                'employee_submitted_at': claim.employee_submitted_at.strftime('%b %d, %Y %H:%M:%S'),
                'manager_action_at': claim.manager_action_at.strftime('%b %d, %Y %H:%M:%S') if claim.manager_action_at else None,
                'manager_action_type': claim.manager_action_type,
                'items': [{
                    'type': item.type,
                    'uom': item.uom,
                    'quantity': str(item.quantity),
                    'amount': str(item.amount),
                } for item in claim.items.all()]
            }
            claims_data.append(claim_data)
        
        return JsonResponse({
            'claims': claims_data,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        })
    
    # Regular request - return full page 
    
    return render(request, 'ajserpadmin/claimrequest.html', context)

# API endpoint for search only
@login_required
def search_claims(request):
    if request.method == 'GET':
        claims = ClaimRequest.objects.select_related('requested_by').prefetch_related('items').all().order_by('-employee_submitted_at')
        
        # Apply filters
        document_no = request.GET.get('document_no', '')
        requested_by = request.GET.get('requested_by', '')
        status = request.GET.get('status', '')
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')
        global_search = request.GET.get('global_search', '')
        
        if document_no:
            claims = claims.filter(document_number__icontains=document_no)
        
        if requested_by:
            claims = claims.filter(requested_by_username_icontains=requested_by)
        
        if status:
            claims = claims.filter(status=status)
        
        if from_date:
            claims = claims.filter(created_at__gte=from_date)
        
        if to_date:
            claims = claims.filter(created_at__lte=to_date)
        
        if global_search:
            claims = claims.filter(
                Q(document_number__icontains=global_search) |
                Q(requested_by_username_icontains=global_search) |
                Q(remarks__icontains=global_search) |
                Q(items_type_icontains=global_search) |
                Q(status__icontains=global_search)
            ).distinct()
        
        # Serialize data
        claims_data = []
        for claim in claims:
            claim_data = {
                'id': claim.id,
                'document_number': claim.document_number,
                'requested_by': claim.requested_by.username,
                'status': claim.status,
                'remarks': claim.remarks or '-',
                'employee_submitted_at': claim.employee_submitted_at.strftime('%b %d, %Y %H:%M:%S'),
                'manager_action_at': claim.manager_action_at.strftime('%b %d, %Y %H:%M:%S') if claim.manager_action_at else None,
                'manager_action_type': claim.manager_action_type,
                'items': [{
                    'type': item.type,
                    'uom': item.uom,
                    'quantity': str(item.quantity),
                    'amount': str(item.amount),
                } for item in claim.items.all()]
            }
            claims_data.append(claim_data)
        
        return JsonResponse({'claims': claims_data})

@login_required
def get_claim_document_numbers(request):
    """API to get document numbers for autocomplete"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'document_numbers': []})
    
    document_numbers = ClaimRequest.objects.filter(
        document_number__icontains=query
    ).values_list('document_number', flat=True).distinct()[:10]
    
    return JsonResponse({
        'document_numbers': list(document_numbers)
})


from .models import VendorInvoice  # Add this import

@login_required
def vendorinvoice(request):
    """Display list of all vendor invoices with search and filtering"""
    vendor_invoices = VendorInvoice.objects.all().order_by('-document_date').prefetch_related('vendor')
    
    # Get filter parameters
    invoice_number = request.GET.get('invoice_number', '')
    vendor_name = request.GET.get('vendor_name', '')
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    q = request.GET.get('q', '')  # Global search parameter
    
    # Apply filters
    if invoice_number:
        vendor_invoices = vendor_invoices.filter(invoice_number__icontains=invoice_number)
    
    if vendor_name:
        vendor_invoices = vendor_invoices.filter(vendor__vendor_name__icontains=vendor_name)
    
    if status:
        vendor_invoices = vendor_invoices.filter(status=status)
    
    if from_date:
        vendor_invoices = vendor_invoices.filter(document_date__gte=from_date)
    
    if to_date:
        vendor_invoices = vendor_invoices.filter(document_date__lte=to_date)
        
    # Global search (search across multiple fields)
    if q:
        vendor_invoices = vendor_invoices.filter(
            models.Q(invoice_number__icontains=q) |
            models.Q(vendor__vendor_name__icontains=q) |
            models.Q(document_number__icontains=q) |
            models.Q(material_service_details__icontains=q)
        )
        
    # Pagination - Show 10 vendor invoices per page
    paginator = Paginator(vendor_invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get vendors for edit modal dropdown
    vendors = Supplier.objects.all()
    
    context = {
        'vendor_invoices': vendor_invoices,
        'page_obj': page_obj,
        'vendors': vendors,  # Add this for edit modal
    }
    
    return render(request, "ajserpadmin/vendorinvoice.html", context)

@login_required
def addvendorinvoice(request):
    """Handle vendor invoice creation"""
    if request.method == 'POST':
        print("💾 VENDOR INVOICE FORM SUBMISSION")
        print("🔍 DEBUG: POST data:", dict(request.POST))
        
        try:
            # Get basic info
            transaction_type = request.POST.get('transaction_type')
            document_date = request.POST.get('document_date')
            vendor_code = request.POST.get('vendor_code')
            payment_terms = request.POST.get('payment_terms')
            invoice_number = request.POST.get('invoice_number')
            invoice_date = request.POST.get('invoice_date')
            hsn_code = request.POST.get('hsn_code')
            material_service_details = request.POST.get('material_service_details')
            uom = request.POST.get('uom')
            quantity = request.POST.get('quantity')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            tax_type = request.POST.get('tax_type')
            cess_applicable = request.POST.get('cess_applicable') == 'on'
            
            # Get calculation fields
            basic_amount = float(request.POST.get('basic_amount', 0))
            cgst_rate = float(request.POST.get('cgst_rate', 0))
            sgst_rate = float(request.POST.get('sgst_rate', 0))
            igst_rate = float(request.POST.get('igst_rate', 0))
            cess_rate = float(request.POST.get('cess_rate', 0))
            discount_amount = float(request.POST.get('discount_amount', 0))
            tds_rate = float(request.POST.get('tds_rate', 0))
            
            # Get uploaded file
            uploaded_images = request.FILES.get('uploaded_images')
            remarks = request.POST.get('remarks', '')
            
            print(f"🔍 DEBUG: Vendor Code: {vendor_code}")
            
            # Get vendor object
            try:
                vendor = Supplier.objects.get(vendor_code=vendor_code)
                print(f"✅ DEBUG: Found vendor: {vendor.vendor_name}")
            except Supplier.DoesNotExist:
                messages.error(request, f'Vendor with code {vendor_code} not found!')
                return redirect('ajserp:addvendorinvoice')
            
            # Create Vendor Invoice
            vendor_invoice = VendorInvoice(
                transaction_type=transaction_type,
                document_date=document_date,
                vendor=vendor,
                payment_terms=payment_terms,
                invoice_number=invoice_number,
                invoice_date=invoice_date,
                hsn_code=hsn_code,
                material_service_details=material_service_details,
                uom=uom,
                quantity=quantity,
                address1=address1,
                address2=address2,
                tax_type=tax_type,
                cess_applicable=cess_applicable,
                basic_amount=basic_amount,
                cgst_rate=cgst_rate,
                sgst_rate=sgst_rate,
                igst_rate=igst_rate,
                cess_rate=cess_rate,
                discount_amount=discount_amount,
                tds_rate=tds_rate,
                uploaded_images=uploaded_images,
                remarks=remarks
            )
            
            # Save to trigger auto-generation and calculations
            vendor_invoice.save()
            
            messages.success(request, f'Vendor Invoice created successfully! Document Number: {vendor_invoice.document_number}')
            return redirect('ajserp:vendorinvoice')
            
        except Exception as e:
            print(f"❌ Error creating vendor invoice: {str(e)}")
            messages.error(request, f'Error creating vendor invoice: {str(e)}')
            return redirect('ajserp:addvendorinvoice')
    
    # GET request - show form
    vendors = Supplier.objects.all()
    
    context = {
        'vendors': vendors,
        'today': datetime.now().date().isoformat()
    }
    return render(request, 'ajserpadmin/addvendorinvoice.html', context)

@login_required
def create_vendor_invoice(request):
    """Handle calculation requests from Save button (JSON only)"""
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            print("🔢 VENDOR INVOICE CALCULATION REQUEST from Save button")
            data = json.loads(request.body)
            
            basic_amount = float(data.get('basic_amount', 0))
            cgst_rate = float(data.get('cgst_rate', 0))
            sgst_rate = float(data.get('sgst_rate', 0))
            igst_rate = float(data.get('igst_rate', 0))
            cess_rate = float(data.get('cess_rate', 0))
            discount_amount = float(data.get('discount_amount', 0))
            tds_rate = float(data.get('tds_rate', 0))
            tax_type = data.get('tax_type', 'CGST')
            cess_applicable = data.get('cess_applicable', False)
            
            print(f"📦 Vendor Invoice Calculation data:")
            print(f"  - Basic Amount: {basic_amount}")
            print(f"  - Tax Type: {tax_type}")
            print(f"  - Cess Applicable: {cess_applicable}")
            
            # Calculate amounts based on tax type
            if tax_type == 'CGST':
                cgst_amount = (basic_amount * cgst_rate) / 100
                sgst_amount = (basic_amount * sgst_rate) / 100
                igst_amount = 0
            else:  # IGST
                igst_amount = (basic_amount * igst_rate) / 100
                cgst_amount = 0
                sgst_amount = 0
            
            # Calculate cess if applicable
            if cess_applicable:
                cess_amount = (basic_amount * cess_rate) / 100
            else:
                cess_amount = 0
            
            # Calculate TDS
            tds_amount = (basic_amount * tds_rate) / 100
            
            # Calculate total amount
            tax_total = cgst_amount + sgst_amount + igst_amount + cess_amount
            total_amount = basic_amount + tax_total - discount_amount - tds_amount
            
            # Round to 2 decimal places
            totals = {
                'cgst_amount': round(cgst_amount, 2),
                'sgst_amount': round(sgst_amount, 2),
                'igst_amount': round(igst_amount, 2),
                'cess_amount': round(cess_amount, 2),
                'tds_amount': round(tds_amount, 2),
                'tax_total': round(tax_total, 2),
                'total_amount': round(total_amount, 2)
            }
            
            print(f"✅ Vendor Invoice Calculation completed: {totals}")
            
            return JsonResponse({
                'success': True,
                'totals': totals
            })
            
        except Exception as e:
            print(f"❌ Vendor Invoice Calculation error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# API Views for Vendor Invoice
@login_required
def vendor_search_autocomplete(request):
    """API for vendor autocomplete"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in both vendor_code and vendor_name
    vendors = Supplier.objects.filter(
        Q(vendor_code__icontains=query) | 
        Q(vendor_name__icontains=query)
    ).values(
        'id', 'vendor_code', 'vendor_name', 
        'billing_address1', 'billing_address2',
        'billing_city', 'billing_state', 'billing_postal_code'
    )[:10]
    
    return JsonResponse(list(vendors), safe=False)

@login_required
def get_vendor_details(request, vendor_id):
    """API to get vendor details for auto-filling address"""
    try:
        vendor = Supplier.objects.get(id=vendor_id)
        data = {
            'vendor_code': vendor.vendor_code,
            'vendor_name': vendor.vendor_name,
            'address1': vendor.billing_address1,
            'address2': vendor.billing_address2 or '',
            'city': vendor.billing_city,
            'state': vendor.billing_state,
            'postal_code': vendor.billing_postal_code,
            'gst_number': vendor.gst_number,
            'success': True
        }
    except Supplier.DoesNotExist:
        data = {
            'success': False,
            'message': 'Vendor not found'
        }
    
    return JsonResponse(data)

@login_required
def edit_vendor_invoice(request, invoice_id):
    """Edit an existing vendor invoice"""
    vendor_invoice = get_object_or_404(VendorInvoice, id=invoice_id)
    
    if request.method == 'POST':
        try:
            print(f"🔧 EDITING VENDOR INVOICE {vendor_invoice.document_number}")
            
            # Get form data
            transaction_type = request.POST.get('transaction_type')
            document_date = request.POST.get('document_date')
            vendor_code = request.POST.get('vendor_code')
            payment_terms = request.POST.get('payment_terms')
            invoice_number = request.POST.get('invoice_number')
            invoice_date = request.POST.get('invoice_date')
            hsn_code = request.POST.get('hsn_code')
            material_service_details = request.POST.get('material_service_details')
            uom = request.POST.get('uom')
            quantity = request.POST.get('quantity')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            tax_type = request.POST.get('tax_type')
            cess_applicable = request.POST.get('cess_applicable') == 'on'
            
            # Get calculation fields
            basic_amount = float(request.POST.get('basic_amount', 0))
            cgst_rate = float(request.POST.get('cgst_rate', 0))
            sgst_rate = float(request.POST.get('sgst_rate', 0))
            igst_rate = float(request.POST.get('igst_rate', 0))
            cess_rate = float(request.POST.get('cess_rate', 0))
            discount_amount = float(request.POST.get('discount_amount', 0))
            tds_rate = float(request.POST.get('tds_rate', 0))
            
            # Get uploaded file
            uploaded_images = request.FILES.get('uploaded_images')
            remarks = request.POST.get('remarks', '')
            
            # Get vendor object
            vendor = Supplier.objects.get(vendor_code=vendor_code)
            
            # Update vendor invoice fields
            vendor_invoice.transaction_type = transaction_type
            vendor_invoice.document_date = document_date
            vendor_invoice.vendor = vendor
            vendor_invoice.payment_terms = payment_terms
            vendor_invoice.invoice_number = invoice_number
            vendor_invoice.invoice_date = invoice_date
            vendor_invoice.hsn_code = hsn_code
            vendor_invoice.material_service_details = material_service_details
            vendor_invoice.uom = uom
            vendor_invoice.quantity = quantity
            vendor_invoice.address1 = address1
            vendor_invoice.address2 = address2
            vendor_invoice.tax_type = tax_type
            vendor_invoice.cess_applicable = cess_applicable
            vendor_invoice.basic_amount = basic_amount
            vendor_invoice.cgst_rate = cgst_rate
            vendor_invoice.sgst_rate = sgst_rate
            vendor_invoice.igst_rate = igst_rate
            vendor_invoice.cess_rate = cess_rate
            vendor_invoice.discount_amount = discount_amount
            vendor_invoice.tds_rate = tds_rate
            vendor_invoice.remarks = remarks
            
            # Update image if provided
            if uploaded_images:
                vendor_invoice.uploaded_images = uploaded_images
            
            # Save to trigger calculations
            vendor_invoice.save()
            
            messages.success(request, f'Vendor Invoice {vendor_invoice.document_number} updated successfully!')
            return redirect('ajserp:vendorinvoice')
            
        except Exception as e:
            print(f"❌ Error updating vendor invoice: {str(e)}")
            messages.error(request, f'Error updating vendor invoice: {str(e)}')
            return redirect('ajserp:vendorinvoice')
    
    # For GET request, show edit form
    vendors = Supplier.objects.all()
    
    context = {
        'vendor_invoice': vendor_invoice,
        'vendors': vendors
    }
    return render(request, 'ajserpadmin/edit_vendor_invoice.html', context)

@login_required
def delete_vendor_invoice(request, invoice_id):
    """Delete a vendor invoice"""
    if request.method == 'POST':
        try:
            vendor_invoice = get_object_or_404(VendorInvoice, id=invoice_id)
            document_number = vendor_invoice.document_number
            vendor_invoice.delete()
            messages.success(request, f'Vendor Invoice {document_number} deleted successfully!')
        except VendorInvoice.DoesNotExist:
            messages.error(request, 'Vendor Invoice not found!')
        except Exception as e:
            messages.error(request, f'Error deleting vendor invoice: {str(e)}')
    
    return redirect('ajserp:vendorinvoice')

@login_required
def get_vendor_invoice_suggestions(request):
    """Get vendor invoice number suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 VENDOR INVOICE SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        vendor_invoices = VendorInvoice.objects.filter(
            invoice_number__icontains=query
        ).values('invoice_number', 'vendor__vendor_name')[:10]
        
        suggestions = []
        for invoice in vendor_invoices:
            suggestions.append({
                'value': invoice['invoice_number'],
                'text': f"{invoice['invoice_number']} - {invoice['vendor__vendor_name']}"
            })
        
        print(f"✅ Found {len(suggestions)} vendor invoice suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_vendor_invoice_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_vendor_name_suggestions(request):
    """Get vendor name suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 VENDOR NAME SUGGESTIONS - Query: '{query}'")
    
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        vendors = Supplier.objects.filter(
            vendor_name__icontains=query
        ).values('vendor_name')[:10]
        
        suggestions = [{'value': vendor['vendor_name'], 'text': vendor['vendor_name']} for vendor in vendors]
        print(f"✅ Found {len(suggestions)} vendor suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_vendor_name_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_vendor_invoice_global_suggestions(request):
    """Get global search suggestions for vendor invoices"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 VENDOR INVOICE GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search vendor invoice numbers
        vendor_invoices = VendorInvoice.objects.filter(invoice_number__icontains=query)[:5]
        for invoice in vendor_invoices:
            suggestions.append({
                'value': invoice.invoice_number,
                'text': f"Vendor Invoice: {invoice.invoice_number} - {invoice.vendor.vendor_name}"
            })
        
        # Search vendor names  
        vendors = Supplier.objects.filter(vendor_name__icontains=query)[:5]
        for vendor in vendors:
            suggestions.append({
                'value': vendor.vendor_name,
                'text': f"Vendor: {vendor.vendor_name}"
            })
        
        print(f"✅ Found {len(suggestions)} vendor invoice global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in get_vendor_invoice_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    

 # Vendor Payment Views
@login_required
def paymentout(request):
    """Display list of all vendor payments"""
    vendor_payments = VendorPayment.objects.all().order_by('-payment_date').select_related('vendor')
    
    # Get filter parameters
    payment_id = request.GET.get('payment_id', '')
    vendor_name = request.GET.get('vendor_name', '')
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    q = request.GET.get('q', '')  # Global search parameter
    
    # Apply filters
    if payment_id:
        vendor_payments = vendor_payments.filter(payment_id__icontains=payment_id)
    
    if vendor_name:
        vendor_payments = vendor_payments.filter(vendor__vendor_name__icontains=vendor_name)
    
    if status:
        vendor_payments = vendor_payments.filter(status=status)
    
    if from_date:
        vendor_payments = vendor_payments.filter(payment_date__gte=from_date)
    
    if to_date:
        vendor_payments = vendor_payments.filter(payment_date__lte=to_date)
        
    # Global search (search across multiple fields)
    if q:
        vendor_payments = vendor_payments.filter(
            models.Q(payment_id__icontains=q) |
            models.Q(vendor__vendor_name__icontains=q) |
            models.Q(document_number__icontains=q) |
            models.Q(mode_of_payment__icontains=q)
        )
        
    # Pagination - Show 10 payments per page
    paginator = Paginator(vendor_payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'vendor_payments': vendor_payments,
        'page_obj': page_obj,
    }
    
    return render(request, "ajserpadmin/paymentout.html", context)

@login_required
def addpaymentsout(request):
    """Handle vendor payment creation"""
    vendors = Supplier.objects.all()
    
    if request.method == 'POST':
        print("💾 VENDOR PAYMENT FORM SUBMISSION")
        print("🔍 DEBUG: POST data:", dict(request.POST))
        
        try:
            # Get form data - CONVERT TO DECIMAL
            payment_type = request.POST.get('payment_type')
            payment_date = request.POST.get('payment_date')
            vendor_code = request.POST.get('vendor_code')
            document_number = request.POST.get('document_number')
            vendor_invoice = request.POST.get('vendor_invoice')
            mode_of_payment = request.POST.get('mode_of_payment')
            payment_reference = request.POST.get('payment_reference')
            
            # ✅ FIX: Convert to Decimal instead of float
            from decimal import Decimal
            due_amount = Decimal(request.POST.get('due_amount', 0))
            payment_amount = Decimal(request.POST.get('payment_amount', 0))
            
            remarks = request.POST.get('remarks', '')
            
            print(f"🔍 DEBUG: Vendor Code: {vendor_code}")
            print(f"🔍 DEBUG: Due Amount (Decimal): {due_amount}")
            print(f"🔍 DEBUG: Payment Amount (Decimal): {payment_amount}")
            
            # Get vendor object
            try:
                vendor = Supplier.objects.get(vendor_code=vendor_code)
                print(f"✅ DEBUG: Found vendor: {vendor.vendor_name}")
            except Supplier.DoesNotExist:
                messages.error(request, f'Vendor with code {vendor_code} not found!')
                return redirect('ajserp:addpaymentsout')
            
            # Create Vendor Payment
            vendor_payment = VendorPayment(
                payment_type=payment_type,
                payment_date=payment_date,
                vendor=vendor,
                document_number=document_number,
                vendor_invoice=vendor_invoice,
                mode_of_payment=mode_of_payment,
                payment_reference=payment_reference,
                due_amount=due_amount,  # Now Decimal, not float
                payment_amount=payment_amount,  # Now Decimal, not float
                remarks=remarks
            )
            
            # Save to trigger auto-generation and calculations
            vendor_payment.save()
            
            # Get the final balance from ledger after payment
            final_balance = vendor_payment.get_balance_after_payment()
            
            messages.success(request, f'Vendor Payment created successfully! Payment ID: {vendor_payment.payment_id}, Balance: ₹{final_balance:,.2f}')
            return redirect('ajserp:paymentout')
            
        except Exception as e:
            print(f"❌ Error creating vendor payment: {str(e)}")
            messages.error(request, f'Error creating vendor payment: {str(e)}')
            return redirect('ajserp:addpaymentsout')
    
    # GET request - show form
    context = {
        'vendors': vendors,
        'today': datetime.now().date().isoformat()
    }
    return render(request, 'ajserpadmin/addpaymentsout.html', context)

@login_required
def get_vendor_due_amount(request):
    """API to get vendor's due amount from ledger (BEFORE any payment)"""
    vendor_code = request.GET.get('vendor_code', '')
    
    if not vendor_code:
        return JsonResponse({
            'success': False,
            'message': 'Vendor code is required'
        })
    
    try:
        vendor = Supplier.objects.get(vendor_code=vendor_code)
        
        # Calculate due amount from ledger using your model logic
        ledger_entries = VendorLedger.objects.filter(vendor_code=vendor_code)
        
        total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
        total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
        
        # Due amount = Total Credit (invoices) - Total Debit (payments)
        due_amount = total_credit - total_debit
        due_amount = max(due_amount, 0)  # Return 0 if negative
        
        data = {
            'vendor_name': vendor.vendor_name,
            'due_amount': float(due_amount),
            'total_credit': float(total_credit),  # Total invoices
            'total_debit': float(total_debit),    # Total payments
            'success': True
        }
        
        print(f"📊 LEDGER CALCULATION for {vendor_code}:")
        print(f"  - Total Invoices (Credit): ₹{total_credit:,.2f}")
        print(f"  - Total Payments (Debit): ₹{total_debit:,.2f}")
        print(f"  - Due Amount: ₹{due_amount:,.2f}")
        
        return JsonResponse(data)
        
    except Supplier.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Vendor not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error calculating due amount: {str(e)}'
        })

@login_required
def get_vendor_balance_after_payment(request):
    """API to calculate balance after a proposed payment"""
    vendor_code = request.GET.get('vendor_code', '')
    payment_amount = float(request.GET.get('payment_amount', 0))
    
    try:
        vendor = Supplier.objects.get(vendor_code=vendor_code)
        
        # Calculate current due amount from ledger
        ledger_entries = VendorLedger.objects.filter(vendor_code=vendor_code)
        
        total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
        total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
        
        # Current due amount (before this payment)
        current_due = total_credit - total_debit
        
        # Balance after this payment
        balance_after = current_due - payment_amount
        
        data = {
            'current_due': float(current_due),
            'balance_after': float(balance_after),
            'success': True
        }
        
        print(f"📊 BALANCE CALCULATION for {vendor_code}:")
        print(f"  - Current Due: ₹{current_due:,.2f}")
        print(f"  - Payment Amount: ₹{payment_amount:,.2f}")
        print(f"  - Balance After: ₹{balance_after:,.2f}")
        
    except Supplier.DoesNotExist:
        data = {
            'success': False,
            'message': 'Vendor not found'
        }
    except Exception as e:
        data = {
            'success': False,
            'message': f'Error calculating balance: {str(e)}'
        }
    
    return JsonResponse(data)

@login_required
def vendor_payment_suggestions(request):
    """API for vendor code/name suggestions in payment form with due amounts"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 VENDOR PAYMENT VENDOR SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        # Search in both vendor_code and vendor_name
        vendors = Supplier.objects.filter(
            Q(vendor_code__icontains=query) | 
            Q(vendor_name__icontains=query)
        ).values('vendor_code', 'vendor_name')[:10]
        
        vendor_list = []
        for vendor in vendors:
            # Calculate due amount for each vendor from VendorLedger
            ledger_entries = VendorLedger.objects.filter(vendor_code=vendor['vendor_code'])
            
            total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
            total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
            
            # Due amount = Total Credit (invoices) - Total Debit (payments)
            due_amount = total_credit - total_debit
            due_amount = max(due_amount, 0)  # Return 0 if negative
            
            vendor_list.append({
                'vendor_code': vendor['vendor_code'],
                'vendor_name': vendor['vendor_name'],
                'due_amount': float(due_amount),
                'display_text': f"{vendor['vendor_code']} - {vendor['vendor_name']} (Due: ₹{due_amount:,.2f})"
            })
        
        print(f"✅ Found {len(vendor_list)} vendor suggestions for payment")
        return JsonResponse(vendor_list, safe=False)
        
    except Exception as e:
        print(f"❌ Error in vendor_payment_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    
@login_required
def get_vendor_payment_details(request):
    """API to get vendor details for payment form"""
    vendor_code = request.GET.get('vendor_code', '')
    
    if not vendor_code:
        return JsonResponse({'success': False, 'message': 'Vendor code is required'})
    
    try:
        vendor = Supplier.objects.get(vendor_code=vendor_code)
        
        # Calculate due amount from ledger
        ledger_entries = VendorLedger.objects.filter(vendor_code=vendor_code)
        
        total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
        total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
        
        # Due amount = Total Credit (invoices) - Total Debit (payments)
        due_amount = total_credit - total_debit
        due_amount = max(due_amount, 0)  # Return 0 if negative
        
        data = {
            'vendor_name': vendor.vendor_name,
            'due_amount': float(due_amount),
            'total_credit': float(total_credit),
            'total_debit': float(total_debit),
            'success': True
        }
        
        print(f"📊 VENDOR PAYMENT DETAILS for {vendor_code}:")
        print(f"  - Vendor Name: {vendor.vendor_name}")
        print(f"  - Due Amount: ₹{due_amount:,.2f}")
        
        return JsonResponse(data)
        
    except Supplier.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Vendor not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error getting vendor details: {str(e)}'
        })

@login_required
def vendor_payment_global_suggestions(request):
    """API for global vendor payment search suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 VENDOR PAYMENT GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search payment IDs
        payments = VendorPayment.objects.filter(payment_id__icontains=query)[:5]
        for payment in payments:
            suggestions.append({
                'value': payment.payment_id,
                'text': f"Payment: {payment.payment_id} - {payment.vendor.vendor_name}"
            })
        
        # Search vendor names  
        vendors = Supplier.objects.filter(vendor_name__icontains=query)[:5]
        for vendor in vendors:
            suggestions.append({
                'value': vendor.vendor_name,
                'text': f"Vendor: {vendor.vendor_name}"
            })
        
        # Search vendor codes
        vendor_codes = Supplier.objects.filter(vendor_code__icontains=query)[:5]
        for vendor in vendor_codes:
            suggestions.append({
                'value': vendor.vendor_code,
                'text': f"Vendor Code: {vendor.vendor_code} - {vendor.vendor_name}"
            })
        
        print(f"✅ Found {len(suggestions)} vendor payment global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in vendor_payment_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    
def get_vendor_documents(request):
    """API endpoint to get documents for a specific vendor"""
    vendor_code = request.GET.get('vendor_code')
    
    print(f"🔍 Document API called with vendor_code: {vendor_code}")
    
    if not vendor_code:
        print("❌ No vendor code provided")
        return JsonResponse({'documents': []})
    
    try:
        # Get all documents for this vendor
        documents = VendorLedger.objects.filter(
            vendor_code=vendor_code
        ).values(
            'document_number',
            'transaction_type',
            'due_amount',
            'date',
            'vendor_name'
        ).order_by('-date')
        
        documents_list = list(documents)
        print(f"✅ Found {len(documents_list)} documents for vendor {vendor_code}")
        
        return JsonResponse({'documents': documents_list})
        
    except Exception as e:
        print(f"❌ Error fetching documents: {e}")
        return JsonResponse({'documents': []})
    


@login_required
def receipts(request):
    """Display list of all customer receipts with search and filters"""
    # Start with all receipts ordered by latest
    customer_receipts = CustomerReceipt.objects.all().order_by('-collection_date', '-created_at')
    
    # Get filter parameters from request
    collection_id = request.GET.get('collection_id', '').strip()
    customer_name = request.GET.get('customer_name', '').strip()
    status = request.GET.get('status', '').strip()
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    q = request.GET.get('q', '').strip()  # Global search parameter
    
    # Apply filters
    if collection_id:
        customer_receipts = customer_receipts.filter(collection_id__icontains=collection_id)
        print(f"🔍 Filtered by collection_id: {collection_id}")
    
    if customer_name:
        customer_receipts = customer_receipts.filter(customer_name__icontains=customer_name)
        print(f"🔍 Filtered by customer_name: {customer_name}")
    
    if status:
        customer_receipts = customer_receipts.filter(status=status)
        print(f"🔍 Filtered by status: {status}")
    
    if from_date:
        customer_receipts = customer_receipts.filter(collection_date__gte=from_date)
        print(f"🔍 Filtered by from_date: {from_date}")
    
    if to_date:
        customer_receipts = customer_receipts.filter(collection_date__lte=to_date)
        print(f"🔍 Filtered by to_date: {to_date}")
        
    # Global search (search across multiple fields)
    if q:
        customer_receipts = customer_receipts.filter(
            Q(collection_id__icontains=q) |
            Q(customer_name__icontains=q) |
            Q(customer_code__icontains=q) |
            Q(payment_method__icontains=q) |
            Q(payment_reference__icontains=q) |
            Q(collected_by__icontains=q)
        )
        print(f"🔍 Global search for: {q}")
        
    # Get total count before pagination
    total_receipts = customer_receipts.count()
    print(f"✅ Found {total_receipts} receipts after filtering")
    
    # Pagination - Show 10 receipts per page
    paginator = Paginator(customer_receipts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_receipts': total_receipts,
    }
    
    return render(request, "ajserpadmin/receipts.html",context)

@login_required
def view_receipt(request, receipt_id):
    """View individual receipt details"""
    receipt = get_object_or_404(CustomerReceipt, id=receipt_id)
    
    context = {
        'receipt': receipt,
    }
    
    return render(request, 'ajserpadmin/view_receipt.html', context)

@login_required
def edit_receipt(request, receipt_id):
    """Edit an existing receipt"""
    receipt = get_object_or_404(CustomerReceipt, id=receipt_id)
    
    if request.method == 'POST':
        try:
            print(f"💾 Editing receipt: {receipt.collection_id}")
            print("🔍 POST data:", dict(request.POST))
            
            # Get form data
            customer_code = request.POST.get('customer_code')
            customer_name = request.POST.get('customer_name')
            collection_date = request.POST.get('collection_date')
            collected_by = request.POST.get('collected_by')
            payment_method = request.POST.get('payment_method')
            amount_collected = request.POST.get('amount_collected')
            payment_reference = request.POST.get('payment_reference')
            status = request.POST.get('status')
            remarks = request.POST.get('remarks')
            
            # Update receipt fields
            receipt.customer_code = customer_code
            receipt.customer_name = customer_name
            receipt.collection_date = collection_date
            receipt.collected_by = collected_by
            receipt.payment_method = payment_method
            receipt.amount_collected = amount_collected
            receipt.payment_reference = payment_reference
            receipt.status = status
            receipt.remarks = remarks
            
            # Save the receipt (this will trigger auto-calculations)
            receipt.save()
            
            messages.success(request, f'Receipt {receipt.collection_id} updated successfully!')
            return redirect('ajserp:receipts')
            
        except Exception as e:
            print(f"❌ Error updating receipt: {str(e)}")
            messages.error(request, f'Error updating receipt: {str(e)}')
            return redirect('ajserp:receipts')
    
    # If GET request, show current values in modal
    return redirect('ajserp:receipts')

@login_required
def delete_receipt(request, receipt_id):
    """Delete a receipt"""
    receipt = get_object_or_404(CustomerReceipt, id=receipt_id)
    
    if request.method == 'POST':
        try:
            collection_id = receipt.collection_id
            receipt.delete()
            
            messages.success(request, f'Receipt {collection_id} deleted successfully!')
            print(f"🗑️ Deleted receipt: {collection_id}")
            
        except Exception as e:
            print(f"❌ Error deleting receipt: {str(e)}")
            messages.error(request, f'Error deleting receipt: {str(e)}')
    
    return redirect('ajserp:receipts')
    
@login_required
def addreceipts(request):
    """Handle customer receipt creation"""
    customers = Customer.objects.all()
    
    if request.method == 'POST':
        print("💾 CUSTOMER RECEIPT FORM SUBMISSION")
        print("🔍 DEBUG: POST data:", dict(request.POST))
        
        try:
            # Get form data - CONVERT TO DECIMAL
            from decimal import Decimal
            
            collected_by = request.POST.get('collected_by')
            collection_date = request.POST.get('collection_date')
            customer_code = request.POST.get('customer_code')
            invoice_numbers = request.POST.getlist('invoice_numbers[]')  # Multiple invoices
            payment_method = request.POST.get('payment_method')
            payment_reference = request.POST.get('payment_reference')
            
            # ✅ Convert to Decimal instead of float
            total_outstanding = Decimal(request.POST.get('total_outstanding', 0))
            amount_collected = Decimal(request.POST.get('amount_collected', 0))
            balance_outstanding = Decimal(request.POST.get('balance_outstanding', 0))
            
            remarks = request.POST.get('remarks', '')
            
            print(f"🔍 DEBUG: Customer Code: {customer_code}")
            print(f"🔍 DEBUG: Total Outstanding (Decimal): {total_outstanding}")
            print(f"🔍 DEBUG: Amount Collected (Decimal): {amount_collected}")
            print(f"🔍 DEBUG: Invoice Numbers: {invoice_numbers}")
            
            # Get customer object
            try:
                customer = Customer.objects.get(customer_code=customer_code)
                print(f"✅ DEBUG: Found customer: {customer.customer_name}")
            except Customer.DoesNotExist:
                messages.error(request, f'Customer with code {customer_code} not found!')
                return redirect('ajserp:addreceipts')
            
            # Create Customer Receipt
            customer_receipt = CustomerReceipt(
                collected_by=collected_by,
                collection_date=collection_date,
                customer_code=customer_code,
                customer_name=customer.customer_name,
                invoice_numbers=invoice_numbers,
                payment_method=payment_method,
                payment_reference=payment_reference,
                total_outstanding=total_outstanding,
                amount_collected=amount_collected,
                balance_outstanding=balance_outstanding,
                remarks=remarks
            )
            
            # Handle file upload
            if 'uploaded_images' in request.FILES:
                customer_receipt.uploaded_images = request.FILES['uploaded_images']
            
            # Save to trigger auto-generation and calculations
            customer_receipt.save()
            
            # ✅ FIX: Use the calculated balance_outstanding field instead
            final_balance = customer_receipt.balance_outstanding
            
            messages.success(request, f'Customer Receipt created successfully! Collection ID: {customer_receipt.collection_id}, Balance: ₹{final_balance:,.2f}')
            return redirect('ajserp:receipts')
            
        except Exception as e:
            print(f"❌ Error creating customer receipt: {str(e)}")
            messages.error(request, f'Error creating customer receipt: {str(e)}')
            return redirect('ajserp:addreceipts')
    
    # GET request - show form
    context = {
        'customers': customers,
        'today': datetime.now().date().isoformat()
    }
    return render(request, 'ajserpadmin/addreceipts.html', context)

@login_required
def get_customer_outstanding_amount(request):
    """API to get customer's outstanding amount from ledger (BEFORE any receipt)"""
    customer_code = request.GET.get('customer_code', '')
    
    if not customer_code:
        return JsonResponse({
            'success': False,
            'message': 'Customer code is required'
        })
    
    try:
        customer = Customer.objects.get(customer_code=customer_code)
        
        # Calculate outstanding amount from ledger using your model logic
        ledger_entries = CustomerLedger.objects.filter(customer_code=customer_code)
        
        total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
        total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
        
        # Outstanding amount = Total Debit (invoices) - Total Credit (receipts)
        outstanding_amount = total_debit - total_credit
        outstanding_amount = max(outstanding_amount, 0)  # Return 0 if negative
        
        data = {
            'customer_name': customer.customer_name,
            'outstanding_amount': float(outstanding_amount),
            'total_debit': float(total_debit),    # Total invoices
            'total_credit': float(total_credit),  # Total receipts
            'success': True
        }
        
        print(f"📊 CUSTOMER LEDGER CALCULATION for {customer_code}:")
        print(f"  - Total Invoices (Debit): ₹{total_debit:,.2f}")
        print(f"  - Total Receipts (Credit): ₹{total_credit:,.2f}")
        print(f"  - Outstanding Amount: ₹{outstanding_amount:,.2f}")
        
        return JsonResponse(data)
        
    except Customer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Customer not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error calculating outstanding amount: {str(e)}'
        })

@login_required
def get_customer_balance_after_receipt(request):
    """API to calculate balance after a proposed receipt"""
    customer_code = request.GET.get('customer_code', '')
    amount_collected = float(request.GET.get('amount_collected', 0))
    
    try:
        customer = Customer.objects.get(customer_code=customer_code)
        
        # Calculate current outstanding amount from ledger
        ledger_entries = CustomerLedger.objects.filter(customer_code=customer_code)
        
        total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
        total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
        
        # Current outstanding amount (before this receipt)
        current_outstanding = total_debit - total_credit
        
        # Balance after this receipt
        balance_after = current_outstanding - amount_collected
        
        data = {
            'current_outstanding': float(current_outstanding),
            'balance_after': float(balance_after),
            'success': True
        }
        
        print(f"📊 CUSTOMER BALANCE CALCULATION for {customer_code}:")
        print(f"  - Current Outstanding: ₹{current_outstanding:,.2f}")
        print(f"  - Amount Collected: ₹{amount_collected:,.2f}")
        print(f"  - Balance After: ₹{balance_after:,.2f}")
        
    except Customer.DoesNotExist:
        data = {
            'success': False,
            'message': 'Customer not found'
        }
    except Exception as e:
        data = {
            'success': False,
            'message': f'Error calculating balance: {str(e)}'
        }
    
    return JsonResponse(data)

@login_required
def customer_receipt_suggestions(request):
    """API for customer code/name suggestions in receipt form with outstanding amounts"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 CUSTOMER RECEIPT SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        # Search in both customer_code and customer_name
        customers = Customer.objects.filter(
            Q(customer_code__icontains=query) | 
            Q(customer_name__icontains=query)
        ).values('customer_code', 'customer_name')[:10]
        
        customer_list = []
        for customer in customers:
            # Calculate outstanding amount for each customer from CustomerLedger
            ledger_entries = CustomerLedger.objects.filter(customer_code=customer['customer_code'])
            
            total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
            total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
            
            # Outstanding amount = Total Debit (invoices) - Total Credit (receipts)
            outstanding_amount = total_debit - total_credit
            outstanding_amount = max(outstanding_amount, 0)  # Return 0 if negative
            
            customer_list.append({
                'customer_code': customer['customer_code'],
                'customer_name': customer['customer_name'],
                'outstanding_amount': float(outstanding_amount),
                'display_text': f"{customer['customer_code']} - {customer['customer_name']} (Outstanding: ₹{outstanding_amount:,.2f})"
            })
        
        print(f"✅ Found {len(customer_list)} customer suggestions for receipt")
        return JsonResponse(customer_list, safe=False)
        
    except Exception as e:
        print(f"❌ Error in customer_receipt_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_customer_receipt_details(request):
    """API to get customer details for receipt form"""
    customer_code = request.GET.get('customer_code', '')
    
    if not customer_code:
        return JsonResponse({'success': False, 'message': 'Customer code is required'})
    
    try:
        customer = Customer.objects.get(customer_code=customer_code)
        
        # Calculate outstanding amount from ledger
        ledger_entries = CustomerLedger.objects.filter(customer_code=customer_code)
        
        total_debit = ledger_entries.aggregate(total_dr=Sum('dr_amount'))['total_dr'] or 0
        total_credit = ledger_entries.aggregate(total_cr=Sum('cr_amount'))['total_cr'] or 0
        
        # Outstanding amount = Total Debit (invoices) - Total Credit (receipts)
        outstanding_amount = total_debit - total_credit
        outstanding_amount = max(outstanding_amount, 0)  # Return 0 if negative
        
        data = {
            'customer_name': customer.customer_name,
            'outstanding_amount': float(outstanding_amount),
            'total_debit': float(total_debit),
            'total_credit': float(total_credit),
            'success': True
        }
        
        print(f"📊 CUSTOMER RECEIPT DETAILS for {customer_code}:")
        print(f"  - Customer Name: {customer.customer_name}")
        print(f"  - Outstanding Amount: ₹{outstanding_amount:,.2f}")
        
        return JsonResponse(data)
        
    except Customer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Customer not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error getting customer details: {str(e)}'
        })

@login_required
def customer_receipt_global_suggestions(request):
    """API for global customer receipt search suggestions"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 CUSTOMER RECEIPT GLOBAL SUGGESTIONS - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # Search collection IDs
        receipts = CustomerReceipt.objects.filter(collection_id__icontains=query)[:5]
        for receipt in receipts:
            suggestions.append({
                'value': receipt.collection_id,
                'text': f"Receipt: {receipt.collection_id} - {receipt.customer_name}"
            })
        
        # Search customer names  
        customers = Customer.objects.filter(customer_name__icontains=query)[:5]
        for customer in customers:
            suggestions.append({
                'value': customer.customer_name,
                'text': f"Customer: {customer.customer_name}"
            })
        
        # Search customer codes
        customer_codes = Customer.objects.filter(customer_code__icontains=query)[:5]
        for customer in customer_codes:
            suggestions.append({
                'value': customer.customer_code,
                'text': f"Customer Code: {customer.customer_code} - {customer.customer_name}"
            })
        
        print(f"✅ Found {len(suggestions)} customer receipt global suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in customer_receipt_global_suggestions: {str(e)}")
        return JsonResponse([], safe=False)

@login_required
def get_customer_invoices(request):
    """API endpoint to get unpaid invoices for a specific customer"""
    customer_code = request.GET.get('customer_code')
    
    print(f"🔍 Customer Invoice API called with customer_code: {customer_code}")
    
    if not customer_code:
        print("❌ No customer code provided")
        return JsonResponse({'invoices': []})
    
    try:
        # Get all unpaid invoices for this customer from CustomerLedger
        invoices = CustomerLedger.objects.filter(
            customer_code=customer_code,
            transaction_type='Invoice',
            cr_amount=0  # Only unpaid invoices
        ).values(
            'document_number',
            'date',
            'dr_amount',
            'reference'
        ).order_by('-date')
        
        invoices_list = list(invoices)
        print(f"✅ Found {len(invoices_list)} unpaid invoices for customer {customer_code}")
        
        return JsonResponse({'invoices': invoices_list})
        
    except Exception as e:
        print(f"❌ Error fetching customer invoices: {e}")
        return JsonResponse({'invoices': []})
    
@login_required
def home_search_suggestions(request):
    """API for home page global search suggestions - SEARCHES EVERYTHING"""
    query = request.GET.get('q', '').strip()
    print(f"🔍 HOME PAGE GLOBAL SEARCH - Query: '{query}'")
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        suggestions = []
        
        # 1. SEARCH CUSTOMERS
        customers = Customer.objects.filter(
            Q(customer_name__icontains=query) | 
            Q(customer_code__icontains=query)
        )[:5]
        
        for customer in customers:
            suggestions.append({
                'type': 'customer',
                'value': customer.customer_name,
                'code': customer.customer_code,
                'text': f"👤 Customer: {customer.customer_name} ({customer.customer_code})",
                'url': reverse('ajserp:customers'),
                'icon': 'fa-user'
            })
        
        # 2. SEARCH SUPPLIERS/VENDORS
        suppliers = Supplier.objects.filter(
            Q(vendor_name__icontains=query) | 
            Q(vendor_code__icontains=query)
        )[:5]
        
        for supplier in suppliers:
            suggestions.append({
                'type': 'supplier', 
                'value': supplier.vendor_name,
                'code': supplier.vendor_code,
                'text': f"🏢 Supplier: {supplier.vendor_name} ({supplier.vendor_code})",
                'url': reverse('ajserp:supliers'),
                'icon': 'fa-truck'
            })
        
        # 3. SEARCH MATERIALS
        materials = Material.objects.filter(
            Q(material_name__icontains=query) | 
            Q(material_code__icontains=query) |
            Q(category__icontains=query)
        )[:5]
        
        for material in materials:
            suggestions.append({
                'type': 'material',
                'value': material.material_name,
                'code': material.material_code,
                'text': f"📦 Material: {material.material_name} ({material.material_code})",
                'url': reverse('ajserp:material'),
                'icon': 'fa-box'
            })
        
        # 4. SEARCH ESTIMATES
        estimates = Estimate.objects.filter(
            Q(estimate_number__icontains=query) |
            Q(customer__customer_name__icontains=query)
        ).select_related('customer')[:5]
        
        for estimate in estimates:
            suggestions.append({
                'type': 'estimate',
                'value': estimate.estimate_number,
                'text': f"📋 Estimate: {estimate.estimate_number} - {estimate.customer.customer_name}",
                'url': reverse('ajserp:estimate'),
                'icon': 'fa-file-invoice'
            })
        
        # 5. SEARCH SALES ORDERS
        sales_orders = SalesOrder.objects.filter(
            Q(order_number__icontains=query) |
            Q(customer__customer_name__icontains=query)
        ).select_related('customer')[:5]
        
        for order in sales_orders:
            suggestions.append({
                'type': 'sales_order',
                'value': order.order_number,
                'text': f"🛒 Sales Order: {order.order_number} - {order.customer.customer_name}",
                'url': reverse('ajserp:salesorders'),
                'icon': 'fa-shopping-cart'
            })
        
        # 6. SEARCH PURCHASE ORDERS
        purchase_orders = PurchaseOrder.objects.filter(
            Q(order_number__icontains=query) |
            Q(vendor__vendor_name__icontains=query)
        ).select_related('vendor')[:5]
        
        for order in purchase_orders:
            suggestions.append({
                'type': 'purchase_order',
                'value': order.order_number,
                'text': f"📥 Purchase Order: {order.order_number} - {order.vendor.vendor_name}",
                'url': reverse('ajserp:purchaseorder'),
                'icon': 'fa-clipboard-list'
            })
        
        # 7. SEARCH SALES INVOICES
        sales_invoices = SalesInvoice.objects.filter(
            Q(invoice_number__icontains=query) |
            Q(customer__customer_name__icontains=query)
        ).select_related('customer')[:5]
        
        for invoice in sales_invoices:
            suggestions.append({
                'type': 'sales_invoice',
                'value': invoice.invoice_number,
                'text': f"🧾 Sales Invoice: {invoice.invoice_number} - {invoice.customer.customer_name}",
                'url': reverse('ajserp:salesinvoice'),
                'icon': 'fa-receipt'
            })
        
        # 8. SEARCH VENDOR INVOICES
        vendor_invoices = VendorInvoice.objects.filter(
            Q(invoice_number__icontains=query) |
            Q(vendor__vendor_name__icontains=query)
        ).select_related('vendor')[:5]
        
        for invoice in vendor_invoices:
            suggestions.append({
                'type': 'vendor_invoice',
                'value': invoice.invoice_number,
                'text': f"📄 Vendor Invoice: {invoice.invoice_number} - {invoice.vendor.vendor_name}",
                'url': reverse('ajserp:vendorinvoice'),
                'icon': 'fa-file-invoice-dollar'
            })
        
        print(f"✅ Found {len(suggestions)} global search suggestions")
        return JsonResponse(suggestions, safe=False)
        
    except Exception as e:
        print(f"❌ Error in home_search_suggestions: {str(e)}")
        return JsonResponse([], safe=False)
    
@login_required
def salesdashboard(request):
    """Sales Dashboard with dynamic data from Tracker model"""
    
    # Get filter parameters
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    tracking_no = request.GET.get('tracking_number')
    status_filter = request.GET.get('status', 'all')
    
    # Filter trackers
    trackers = Tracker.objects.all()
    
    if date_from and date_to:
        trackers = trackers.filter(created_at__date__range=[date_from, date_to])
    
    if tracking_no:
        trackers = trackers.filter(tracker_no__icontains=tracking_no)
    
    if status_filter != 'all':
        trackers = trackers.filter(status=status_filter)
    
    # Dashboard statistics - DYNAMIC DATA
    total_tasks = trackers.count()
    completed_tasks = trackers.filter(status='completed').count()
    pending_tasks = trackers.filter(status='pending').count()
    
    # Collection data (you can customize these based on your business logic)
    collection_total = 5000  # Replace with actual calculation from your models
    collection_target = 7000
    advance_requested = 5
    claim_requested = 3
    
    context = {
        'trackers': trackers,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'collection_total': collection_total,
        'collection_target': collection_target,
        'advance_requested': advance_requested,
        'claim_requested': claim_requested,
        'search_params': request.GET,  # Pass search parameters back to template
    }
    return render(request, 'ajserpadmin/salesdashboard.html', context)

@login_required
def check_in_out(request, tracker_id):
    """Handle check-in/check-out functionality"""
    if request.method == 'POST':
        try:
            tracker = Tracker.objects.get(id=tracker_id)
            action = request.POST.get('action')
            
            # Get or create work session for today
            today = timezone.now().date()
            work_session, created = WorkSession.objects.get_or_create(
                tracker=tracker,
                user=request.user,
                login_time__date=today,
                defaults={'login_time': timezone.now()}
            )
            
            if action == 'check_in':
                work_session.check_in_time = timezone.now()
                work_session.session_status = 'checked_in'
                work_session.save()
                
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Successfully checked in',
                    'action': 'checked_in'
                })
            
            elif action == 'check_out':
                work_completion = request.POST.get('work_completion', '')
                
                # Handle image upload
                image = request.FILES.get('image')
                
                work_session.check_out_time = timezone.now()
                work_session.logout_time = timezone.now()
                work_session.work_completion = work_completion
                work_session.session_status = 'checked_out'
                
                if image:
                    work_session.image = image
                    
                work_session.save()
                
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Successfully checked out',
                    'action': 'checked_out'
                })
            
        except Tracker.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Tracker not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# def salesinvoicepdf(request, invoice_id):
#     try:
       
#         sales_invoice = SalesInvoice.objects.get(id=invoice_id)
#         warehouse = sales_invoice.warehouse

#         expiry_date = sales_invoice.date + timedelta(days=30)

#         items = []
#         for item in sales_invoice.sales_invoice_items.all():
#             basic_amount = item.amount or 0
#             line_tax = (
#                 (item.cgst_amount or 0) +
#                 (item.sgst_amount or 0) +
#                 (item.igst_amount or 0) +
#                 (item.cess_amount or 0)
#             )
#             rate_per_unit = (basic_amount / item.quantity) if item.quantity else 0

#             if item.igst_rate:
#                 gst_rate_display = f"IGST {item.igst_rate}%"
#             else:
#                 gst_rate_display = f"CGST {item.cgst_rate}% + SGST {item.sgst_rate}%"
#                 if item.cess_rate:
#                     gst_rate_display += f" + CESS {item.cess_rate}%"

#             items.append({
#                 "material_name": item.material_name,
#                 "description": getattr(item, "description", ""),
#                 "hsn_code": item.material.hsn_code if item.material else "",
#                 "quantity": item.quantity,
#                 "mrp": item.mrp,
#                 "discount": item.discount,
#                 "basic_amount": basic_amount,
#                 "taxable_amount": basic_amount,
#                 "rate": rate_per_unit,
#                 "tax_rate_display": gst_rate_display,
#                 "tax_amount": line_tax,
#                 "amount": basic_amount + line_tax,
#             })
#         total_qty = sum(i.quantity for i in sales_invoice.sales_invoice_items.all())
#         total_tax_amount = sum(
#     (item.cgst_amount or 0) +
#     (item.sgst_amount or 0) +
#     (item.igst_amount or 0) +
#     (item.cess_amount or 0)
#     for item in sales_invoice.sales_invoice_items.all()
# )
#         gst_summary = {}
#         for item in sales_invoice.sales_invoice_items.all():
#             key = (
#                 float(item.cgst_rate or 0),
#                 float(item.sgst_rate or 0),
#                 float(item.igst_rate or 0),
#                 float(item.cess_rate or 0)
#             )

#             if key not in gst_summary:
#                 gst_summary[key] = {
#                     "taxable": 0, "cgst": 0, "sgst": 0, "igst": 0, "cess": 0
#                 }

#             gst_summary[key]["taxable"] += item.amount or 0
#             gst_summary[key]["cgst"] += item.cgst_amount or 0
#             gst_summary[key]["sgst"] += item.sgst_amount or 0
#             gst_summary[key]["igst"] += item.igst_amount or 0
#             gst_summary[key]["cess"] += item.cess_amount or 0

#         total_taxable_amount = sales_invoice.taxable_amount
#         grand_total = sales_invoice.grand_total

#         def amount_words(num):
#             try:
#                 return num2words(int(num), lang="en_IN").title() + " Rupees"
#             except:
#                 return str(num)

#         context = {
#             "sales_invoice": sales_invoice,
#             "warehouse": warehouse,
#             "expiry_date": expiry_date.strftime("%d/%m/%Y"),
#             "items": items,
#             "item_count": len(items),
#             "total_qty": total_qty,
#             "total_tax_amount": total_tax_amount, 
#             "total_taxable_amount": total_taxable_amount,
#             "grand_total": grand_total,
#             "gst_summary": gst_summary,
#             "amount_in_words": amount_words(grand_total),
#         }

#         # ✔ Render template BEFORE PDF creation
#         html_string = render_to_string("ajserpadmin/salesinvoicepdf.html", context)

#         # ✔ Print final HTML for debugging
#         print("\n-------------------- FINAL HTML OUTPUT --------------------\n")
#         print(html_string)
#         print("\n-----------------------------------------------------------\n")

#         # ✔ Create PDF
#         result = BytesIO()
#         pdf = pisa.pisaDocument(BytesIO(html_string.encode("utf-8")), result)

#         if pdf.err:
#             return HttpResponse("PDF Generation Error", status=500)

#         # ✔ Return PDF in browser
#         response = HttpResponse(result.getvalue(), content_type="application/pdf")
#         response["Content-Disposition"] = (
#             f'attachment; filename="sales_invoice_{sales_invoice.invoice_number}.pdf"'
#         )
#         return response

#     except Exception as e:
#         return HttpResponse(f"Error: {e}")

def salesinvoicepdf(request, invoice_id):
    try:
        sales_invoice = SalesInvoice.objects.get(id=invoice_id)
        warehouse = sales_invoice.warehouse
        expiry_date = sales_invoice.date + timedelta(days=30)

        items = []
        for item in sales_invoice.sales_invoice_items.all():

            basic_amount = item.amount or 0

            line_tax = (
                (item.cgst_amount or 0) +
                (item.sgst_amount or 0) +
                (item.igst_amount or 0) +
                (item.cess_amount or 0)
            )

            rate_per_unit = (basic_amount / item.quantity) if item.quantity else 0

            # ---------------------------------------------------------
            #  GST PERCENT DISPLAY (NO DECIMAL & ONLY % SYMBOL)
            # ---------------------------------------------------------
            if item.igst_rate and item.igst_rate > 0:
                # IGST CASE
                gst_rate_display = f"{int(item.igst_rate)}%"
            else:
                gst_parts = []

                if item.cgst_rate and item.cgst_rate > 0:
                    gst_parts.append(f"{int(item.cgst_rate)}%")

                if item.sgst_rate and item.sgst_rate > 0:
                    gst_parts.append(f"{int(item.sgst_rate)}%")

                if item.cess_rate and item.cess_rate > 0:
                    gst_parts.append(f"{int(item.cess_rate)}%")

                gst_rate_display = " + ".join(gst_parts)

            # ---------------------------------------------------------

            items.append({
                "material_name": item.material_name,
                "description": getattr(item, "description", ""),
                "hsn_code": item.material.hsn_code if item.material else "",
                "quantity": item.quantity,
                "mrp": item.mrp,
                "discount": item.discount,
                "basic_amount": basic_amount,
                "taxable_amount": basic_amount,
                "rate": rate_per_unit,
                "tax_rate_display": gst_rate_display,     # <── USED IN HTML
                "tax_amount": line_tax,
                "amount": basic_amount + line_tax,
            })

        # TOTAL QTY
        total_qty = sum(i.quantity for i in sales_invoice.sales_invoice_items.all())

        # TOTAL TAX
        total_tax_amount = sum(
            (item.cgst_amount or 0) +
            (item.sgst_amount or 0) +
            (item.igst_amount or 0) +
            (item.cess_amount or 0)
            for item in sales_invoice.sales_invoice_items.all()
        )

        # GST SUMMARY BOX
        gst_summary = {}
        for item in sales_invoice.sales_invoice_items.all():
            key = (
                float(item.cgst_rate or 0),
                float(item.sgst_rate or 0),
                float(item.igst_rate or 0),
                float(item.cess_rate or 0)
            )

            if key not in gst_summary:
                gst_summary[key] = {"taxable": 0, "cgst": 0, "sgst": 0, "igst": 0, "cess": 0}

            gst_summary[key]["taxable"] += item.amount or 0
            gst_summary[key]["cgst"] += item.cgst_amount or 0
            gst_summary[key]["sgst"] += item.sgst_amount or 0
            gst_summary[key]["igst"] += item.igst_amount or 0
            gst_summary[key]["cess"] += item.cess_amount or 0

        total_taxable_amount = sales_invoice.taxable_amount
        grand_total = sales_invoice.grand_total

        def amount_words(num):
            try:
                return num2words(int(num), lang="en_IN").title() + " Rupees"
            except:
                return str(num)

        context = {
            "sales_invoice": sales_invoice,
            "warehouse": warehouse,
            "expiry_date": expiry_date.strftime("%d/%m/%Y"),
            "items": items,
            "item_count": len(items),
            "total_qty": total_qty,
            "total_tax_amount": total_tax_amount,
            "total_taxable_amount": total_taxable_amount,
            "grand_total": grand_total,
            "gst_summary": gst_summary,
            "amount_in_words": amount_words(grand_total),
        }

        html_string = render_to_string("ajserpadmin/salesinvoicepdf.html", context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("utf-8")), result)

        if pdf.err:
            return HttpResponse("PDF Generation Error", status=500)

        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="sales_invoice_{sales_invoice.invoice_number}.pdf"'
        )
        return response

    except Exception as e:
        return HttpResponse(f"Error: {e}")

def purchaseorderpdf(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
        warehouse = purchase_order.warehouse
        expiry_date = purchase_order.date + timedelta(days=30)

        items = []
        for item in purchase_order.purchase_order_items.all():

            basic_amount = item.amount or 0

            line_tax = (
                (item.cgst_amount or 0) +
                (item.sgst_amount or 0) +
                (item.igst_amount or 0) +
                (item.cess_amount or 0)
            )

            rate_per_unit = (basic_amount / item.quantity) if item.quantity else 0

            # GST DISPLAY
            if item.igst_rate and item.igst_rate > 0:
                gst_rate_display = f"{int(item.igst_rate)}%"
            else:
                gst_parts = []
                if item.cgst_rate and item.cgst_rate > 0:
                    gst_parts.append(f"{int(item.cgst_rate)}%")
                if item.sgst_rate and item.sgst_rate > 0:
                    gst_parts.append(f"{int(item.sgst_rate)}%")
                if item.cess_rate and item.cess_rate > 0:
                    gst_parts.append(f"{int(item.cess_rate)}%")
                gst_rate_display = " + ".join(gst_parts)

            items.append({
                "material_name": item.material_name,
                "description": getattr(item, "description", ""),
                "hsn_code": item.material.hsn_code if item.material else "",
                "quantity": item.quantity,
                "rate": rate_per_unit,
                "mrp": item.mrp,
                "discount": item.discount,
                "basic_amount": basic_amount,
                "taxable_amount": basic_amount,
                "tax_rate_display": gst_rate_display,
                "tax_amount": line_tax,
                "amount": basic_amount + line_tax,
            })

        total_qty = sum(i.quantity for i in purchase_order.purchase_order_items.all())

        total_tax_amount = sum(
            (item.cgst_amount or 0) +
            (item.sgst_amount or 0) +
            (item.igst_amount or 0) +
            (item.cess_amount or 0)
            for item in purchase_order.purchase_order_items.all()
        )

        # GST SUMMARY
        gst_summary = {}
        for item in purchase_order.purchase_order_items.all():
            key = (
                float(item.cgst_rate or 0),
                float(item.sgst_rate or 0),
                float(item.igst_rate or 0),
                float(item.cess_rate or 0)
            )
            if key not in gst_summary:
                gst_summary[key] = {"taxable": 0, "cgst": 0, "sgst": 0, "igst": 0, "cess": 0}

            gst_summary[key]["taxable"] += item.amount or 0
            gst_summary[key]["cgst"] += item.cgst_amount or 0
            gst_summary[key]["sgst"] += item.sgst_amount or 0
            gst_summary[key]["igst"] += item.igst_amount or 0
            gst_summary[key]["cess"] += item.cess_amount or 0

        total_taxable_amount = purchase_order.taxable_amount
        grand_total = purchase_order.grand_total

        def amount_words(num):
            try:
                return num2words(int(num), lang="en_IN").title() + " Rupees"
            except:
                return str(num)

        context = {
            "purchase_order": purchase_order,
            "warehouse": warehouse,
            "expiry_date": expiry_date.strftime("%d/%m/%Y"),
            "items": items,
            "item_count": len(items),
            "total_qty": total_qty,
            "total_tax_amount": total_tax_amount,
            "total_taxable_amount": total_taxable_amount,
            "grand_total": grand_total,
            "gst_summary": gst_summary,
            "amount_in_words": amount_words(grand_total),
        }

        html_string = render_to_string("ajserpadmin/purchaseorderpdf.html", context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("utf-8")), result)

        if pdf.err:
            return HttpResponse("PDF Generation Error", status=500)

        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="purchase_order_{purchase_order.id}.pdf"'
        )
        return response

    except Exception as e:
        return HttpResponse(f"Error: {e}")

def receipt_pdf(request, receipt_id):
    try:
        receipt = CustomerReceipt.objects.get(id=receipt_id)

        # Warehouse (if exists)
        try:
            warehouse = receipt.warehouse
        except:
            warehouse = None

        context = {
            "receipt": receipt,
            "warehouse": warehouse,
        }

        html_string = render_to_string("ajserpadmin/receiptpdf.html", context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("utf-8")), result)

        if pdf.err:
            return HttpResponse("PDF Generation Error", status=500)

        file_name = f"receipt_{receipt.collection_id or receipt.id}.pdf"

        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename=\"{file_name}\"'
        return response

    except Exception as e:
        return HttpResponse(f"Error: {e}")

def salesorder_pdf(request, so_id):
    try:
        sales_order = SalesOrder.objects.get(id=so_id)
        customer = getattr(sales_order, "customer", None)
        billing_address = getattr(sales_order, "billing_address", None)
        shipping_address = getattr(sales_order, "shipping_address", None)
        expiry_date = sales_order.date + timedelta(days=30) if getattr(sales_order, "date", None) else None

        items = []
        # iterate over related line items (adjust relation name if different)
        for item in sales_order.sales_order_items.all():
            basic_amount = item.amount or 0

            line_tax = (
                (item.cgst_amount or 0) +
                (item.sgst_amount or 0) +
                (item.igst_amount or 0) +
                (item.cess_amount or 0)
            )

            rate_per_unit = (basic_amount / item.quantity) if item.quantity else 0

            # GST DISPLAY
            if item.igst_rate and item.igst_rate > 0:
                gst_rate_display = f"{int(item.igst_rate)}%"
            else:
                gst_parts = []
                if item.cgst_rate and item.cgst_rate > 0:
                    gst_parts.append(f"{int(item.cgst_rate)}%")
                if item.sgst_rate and item.sgst_rate > 0:
                    gst_parts.append(f"{int(item.sgst_rate)}%")
                if item.cess_rate and item.cess_rate > 0:
                    gst_parts.append(f"{int(item.cess_rate)}%")
                gst_rate_display = " + ".join(gst_parts)

            items.append({
                "material_name": item.material_name,
                "description": getattr(item, "description", ""),
                "hsn_code": item.material.hsn_code if getattr(item, "material", None) else "",
                "quantity": item.quantity,
                "rate": rate_per_unit,
                "mrp": getattr(item, "mrp", ""),
                "discount": getattr(item, "discount", 0),
                "basic_amount": basic_amount,
                "taxable_amount": basic_amount,
                "tax_rate_display": gst_rate_display,
                "tax_amount": line_tax,
                "amount": basic_amount + line_tax,
            })

        total_qty = sum(i.quantity for i in sales_order.sales_order_items.all())

        total_tax_amount = sum(
            (item.cgst_amount or 0) +
            (item.sgst_amount or 0) +
            (item.igst_amount or 0) +
            (item.cess_amount or 0)
            for item in sales_order.sales_order_items.all()
        )

        # GST SUMMARY
        gst_summary = {}
        for item in sales_order.sales_order_items.all():
            key = (
                float(item.cgst_rate or 0),
                float(item.sgst_rate or 0),
                float(item.igst_rate or 0),
                float(item.cess_rate or 0)
            )
            if key not in gst_summary:
                gst_summary[key] = {"taxable": 0, "cgst": 0, "sgst": 0, "igst": 0, "cess": 0}

            gst_summary[key]["taxable"] += item.amount or 0
            gst_summary[key]["cgst"] += item.cgst_amount or 0
            gst_summary[key]["sgst"] += item.sgst_amount or 0
            gst_summary[key]["igst"] += item.igst_amount or 0
            gst_summary[key]["cess"] += item.cess_amount or 0

        # Use fields on SalesOrder if available (fallback to computed)
        total_taxable_amount = getattr(sales_order, "taxable_amount", sum(i["basic_amount"] for i in items))
        grand_total = getattr(sales_order, "grand_total", sum(i["amount"] for i in items))

        def amount_words(num):
            try:
                return num2words(int(num), lang="en_IN").title() + " Rupees"
            except:
                return str(num)

        context = {
            "sales_order": sales_order,
            "customer": customer,
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "expiry_date": expiry_date.strftime("%d/%m/%Y") if expiry_date else "",
            "items": items,
            "item_count": len(items),
            "total_qty": total_qty,
            "total_tax_amount": total_tax_amount,
            "total_taxable_amount": total_taxable_amount,
            "grand_total": grand_total,
            "gst_summary": gst_summary,
            "amount_in_words": amount_words(grand_total),
        }

        html_string = render_to_string("ajserpadmin/salesorderpdf.html", context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("utf-8")), result)

        if pdf.err:
            return HttpResponse("PDF Generation Error", status=500)

        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="sales_order_{sales_order.id}.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
@login_required
def logout(request):
    auth_logout(request)
    return redirect("ajserp:login")





