from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


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
    return render(request, 'ajserpadmin/dashboard.html')  

def allproducts(request):
    return render(request, "ajserpadmin/allproducts.html")

def warehouse(request):
    return render(request, 'ajserpadmin/warehouse.html')

def icon_menu(request):
    return render(request, "ajserpadmin/icon-menu.html")

def addcustomers(request):
    return render(request, "ajserpadmin/addcustomers.html")

def customers(request):
    return render(request, "ajserpadmin/customers.html")

def addgroups(request):
    return render(request, "ajserpadmin/addgroups.html")

def addmaterial(request):
    return render(request, "ajserpadmin/addmaterial.html")

def addpricelists(request):
    return render(request, "ajserpadmin/addpricelists.html")

def addsupliers(request):
    return render(request, "ajserpadmin/addsupliers.html")

def addwarehouse(request):
    return render(request, "ajserpadmin/addwarehouse.html")

def material(request):
    return render(request, "ajserpadmin/material.html")

def fontawesomeicons(request):
    return render(request, "ajserpadmin/fontawesomeicons.html")

def groups(request):
    return render(request, "ajserpadmin/groups.html")

def pricelists(request):
    return render(request, "ajserpadmin/pricelists.html")

def supliers(request):
    return render(request, "ajserpadmin/supliers.html")

def estimate(request):
    return render(request, "ajserpadmin/estimate.html")

def purchaseorder(request):
    return render(request, "ajserpadmin/purchaseorder.html")

def purchasereturn(request):
    return render(request, "ajserpadmin/purchasereturn.html")

def salesorders(request):
    return render(request, "ajserpadmin/salesorders.html")

def salesinvoice(request):
    return render(request, "ajserpadmin/salesinvoice.html")

def deliverychallans(request):
    return render(request, "ajserpadmin/deliverychallans.html")

def salesreturn(request):
    return render(request, "ajserpadmin/salesreturn.html")

def creditnote(request):
    return render(request, "ajserpadmin/creditnote.html")

def expenses(request):
    return render(request, "ajserpadmin/expenses.html")

def receipts(request):
    return render(request, "ajserpadmin/receipts.html")

def paymentout(request):
    return render(request, "ajserpadmin/paymentout.html")

def vendorinvoice(request):
    return render(request, "ajserpadmin/vendorinvoice.html")

def commonform(request):
    return render(request, "ajserpadmin/commonform.html")

def creditnote(request):
    return render(request, "ajserpadmin/creditnote.html")

def addexpense(request):
    return render(request, "ajserpadmin/addexpense.html")

def addreceipts(request):
    return render(request, "ajserpadmin/addreceipts.html")

def addpaymentsout(request):
    return render(request, "ajserpadmin/addpaymentsout.html")

def addvendorinvoice(request):
    return render(request, "ajserpadmin/addvendorinvoice.html")

def claimapproval(request):
    return render(request, "ajserpadmin/claimapproval.html")

def claimrequest(request):
    return render(request, "ajserpadmin/claimrequest.html")

def addclaimapproval(request):
    return render(request, "ajserpadmin/addclaimapproval.html")

def materialinward(request):
    return render(request, "ajserpadmin/materialinward.html")

def addmaterialinward(request):
    return render(request, "ajserpadmin/addmaterialinward.html")

def addsalesinvoice(request):
    return render(request, "ajserpadmin/addsalesinvoice.html")

def addsalesorders(request):
    return render(request, "ajserpadmin/addsalesorders.html")

def taxmaster(request):
    return render(request, "ajserpadmin/taxmaster.html")

def user(request):
    return render(request, "ajserpadmin/user.html")

def addpurchaseorder(request):
    return render(request, "ajserpadmin/addpurchaseorder.html")

def addpurchasereturn(request):
    return render(request, "ajserpadmin/addpurchasereturn.html")

def profile(request):
    return render(request, "ajserpadmin/profile.html")

def report(request):
    return render(request, "ajserpadmin/report.html")

def logout(request):
    auth_logout(request)
    return redirect("ajserp:login")




