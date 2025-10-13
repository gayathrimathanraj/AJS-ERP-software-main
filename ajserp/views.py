from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Material, Taxes, Warehouse, Customer
from .forms import MaterialForm, TaxesForm, WarehouseForm,CustomerForm


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

@login_required
def addgroups(request):
    return render(request, "ajserpadmin/addgroups.html")

@login_required
def addmaterial(request):
    return render(request, "ajserpadmin/addmaterial.html")

@login_required
def addpricelists(request):
    return render(request, "ajserpadmin/addpricelists.html")

@login_required
def addsupliers(request):
    return render(request, "ajserpadmin/addsupliers.html")

# @login_required
# def addwarehouse(request):
#     return render(request, "ajserpadmin/addwarehouse.html")

@login_required
def material(request):
    return render(request, "ajserpadmin/material.html")

@login_required
def fontawesomeicons(request):
    return render(request, "ajserpadmin/fontawesomeicons.html")

@login_required
def groups(request):
    return render(request, "ajserpadmin/groups.html")

@login_required
def pricelists(request):
    return render(request, "ajserpadmin/pricelists.html")

@login_required
def supliers(request):
    return render(request, "ajserpadmin/supliers.html")

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

@login_required
def materialinward(request):
    return render(request, "ajserpadmin/materialinward.html")

@login_required
def addmaterialinward(request):
    return render(request, "ajserpadmin/addmaterialinward.html")

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
    taxes = Taxes.objects.all()
    if request.method == 'POST':
        form = TaxesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ajserp:taxmaster')
    else:
        form = TaxesForm()
    return render(request, 'ajserpadmin/taxmaster.html', {'form': form, 'taxes': taxes})

@login_required
def addmaterial(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("✅ Material saved successfully!")
            return redirect('ajserp:material')
        else:
            print("❌ Form errors:", form.errors)
    else:
        form = MaterialForm()
    
    # PASS THE FORM TO TEMPLATE
    return render(request, 'ajserpadmin/addmaterial.html', {'form': form})

# FIXED: Add login_required decorator
@login_required
def material(request):
    materials = Material.objects.select_related('taxes').all()
    return render(request, 'ajserpadmin/material.html', {'materials': materials})

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
def addwarehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        print("✅ Form data received:", request.POST)  # ADD THIS
        if form.is_valid():
            form.save()
            print("✅ Warehouse saved successfully!")  # ADD THIS
            return redirect('ajserp:warehouse')
        else:
            print("❌ Form errors:", form.errors)  # ADD THIS
    else:
        form = WarehouseForm()
    return render(request, 'ajserpadmin/addwarehouse.html', {'form': form})

# Customer List View
@login_required
def customers(request):
    customers = Customer.objects.all()
    return render(request, 'ajserpadmin/customers.html', {'customers': customers})

# Add Customer View
# @login_required
# def addcustomers(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('ajserp:customers')
#         else:
#             print("❌ Customer form errors:", form.errors)
#     else:
#         form = CustomerForm()
#     return render(request, 'ajserpadmin/addcustomers.html', {'form': form})

@login_required
def addcustomers(request):
    if request.method == 'POST':
        # DEBUG: Print what we're receiving
        print("✅ Received POST data:", dict(request.POST))
        print("✅ Checkbox value:", request.POST.get('same_as_billing'))
        
        post_data = request.POST.copy()
        same_as_billing = post_data.get('same_as_billing') == 'on'
        print("✅ Same as billing:", same_as_billing)
        
        if same_as_billing:
            print("✅ Copying billing to shipping...")
            # Copy billing to shipping
            post_data['shipping_address1'] = post_data.get('billing_address1', '')
            post_data['shipping_city'] = post_data.get('billing_city', '')
            post_data['shipping_state'] = post_data.get('billing_state', '')
            post_data['shipping_country'] = post_data.get('billing_country', '')
            post_data['shipping_postal_code'] = post_data.get('billing_postal_code', '')
            print("✅ After copying:", {k: v for k, v in post_data.items() if 'shipping' in k})
        
        form = CustomerForm(post_data, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('ajserp:customers')
        else:
            print("❌ Customer form errors:", form.errors)
    else:
        form = CustomerForm()
    
    return render(request, 'ajserpadmin/addcustomers.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect("ajserp:login")





