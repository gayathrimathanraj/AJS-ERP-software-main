from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'ajserpadmin/dashboard.html')  

def allproducts(request):
    return render(request, "ajserpadmin/allproducts.html")

def warehouse(request):
    return render(request, 'ajserpadmin/warehouse.html')

def icon_menu(request):
    return render(request, "ajserpadmin/icon-menu.html")

def customers(request):
    return render(request, "ajserpadmin/addcustomer.html")

def addcustomer(request):
    return render(request, "ajserpadmin/customers.html")

def addgroups(request):
    return render(request, "ajserpadmin/addgroups.html")

def additems(request):
    return render(request, "ajserpadmin/additems.html")

def addpricelists(request):
    return render(request, "ajserpadmin/addpricelists.html")

def addsupliers(request):
    return render(request, "ajserpadmin/addsupliers.html")

def addwarehouse(request):
    return render(request, "ajserpadmin/addwarehouse.html")

def allitems(request):
    return render(request, "ajserpadmin/allitems.html")

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

def purchaseinvoice(request):
    return render(request, "ajserpadmin/purchaseinvoice.html")

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




