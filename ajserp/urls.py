from django.urls import path
from . import views

app_name="ajserp"

urlpatterns = [

    path("", views.index, name="dashboard"), 
    path("all-products/", views.allproducts, name="allproducts"),
    path("warehouse/", views.warehouse, name="warehouse"),
    path("icon-menu/", views.icon_menu, name="icon_menu"),
    path("addcustomer/", views.addcustomer, name="addcustomer"),
    path("customers/", views.customers, name="customers"),
    path("addgroups/", views.addgroups, name="addgroups"),
    path("additems/", views.additems, name="additems"),
    path("addpricelists/", views.addpricelists, name="addpricelists"),
    path("addsupliers/", views.addsupliers, name="addsupliers"),
    path("addwarehouse/", views.addwarehouse, name="addwarehouse"),
    path("allitems/", views.allitems, name="allitems"),
    path("fontawesomeicons/", views.fontawesomeicons, name="fontawesomeicons"),
    path("groups/", views.groups, name="groups"),
    path("pricelists/", views.pricelists, name="pricelists"),
    path("supliers/", views.supliers, name="supliers"),
    path("estimate/", views.estimate, name="estimate"),
    path("purchaseorder/", views.purchaseorder, name="purchaseorder"),
    path("purchaseinvoice/", views.purchaseinvoice, name="purchaseinvoice"),
    path("purchasereturn/", views.purchasereturn, name="purchasereturn"),
    path("salesorders/", views.salesorders, name="salesorders"),
    path("salesinvoice/", views.salesinvoice, name="salesinvoice"),
    path("deliverychallans/", views.deliverychallans, name="deliverychallans"),
    path("salesreturn/", views.salesreturn, name="salesreturn"),
    path("creditnote/", views.creditnote, name="creditnote"),
    path("addexpense/", views.addexpense, name="addexpense"),
    path("expenses/", views.expenses, name="expenses"),
    path("receipts/", views.receipts, name="receipts"),
    path("paymentout/", views.paymentout, name="paymentout"),
    path("vendorinvoice/", views.vendorinvoice, name="vendorinvoice"),
    path("commonform/", views.commonform, name="commonform"),
    path("creditnote/", views.creditnote, name="creditnote"),
    path('addreceipts/', views.addreceipts, name='addreceipts'),
    path('addpaymentsout/', views.addpaymentsout, name='addpaymentsout'),
    path('addvendorinvoice/', views.addvendorinvoice, name='addvendorinvoice')
    
    
    

]