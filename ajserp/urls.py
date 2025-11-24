from django.urls import path
from . import views


app_name="ajserp"

urlpatterns = [

    path("", views.index, name="dashboard"), 
    path("all-products/", views.allproducts, name="allproducts"),
    path("warehouse/", views.warehouse, name="warehouse"),
    path("icon-menu/", views.icon_menu, name="icon_menu"),
    path("addcustomers/", views.addcustomers, name="addcustomers"),
    path("customers/", views.customers, name="customers"),
    path("addgroups/", views.addgroups, name="addgroups"),
    path("addmaterial/", views.addmaterial, name="addmaterial"),
    path("addpricelists/", views.addpricelists, name="addpricelists"),
    path("addsupliers/", views.addsupliers, name="addsupliers"),
    path("addwarehouse/", views.addwarehouse, name="addwarehouse"),
    path("material/", views.material, name="material"),
    path("fontawesomeicons/", views.fontawesomeicons, name="fontawesomeicons"),
    # path("groups/", views.groups, name="groups"),
    path("pricelists/", views.pricelists, name="pricelists"),
    path("supliers/", views.supliers, name="supliers"),
    path("estimate/", views.estimate, name="estimate"),
    path("purchaseorder/", views.purchaseorder, name="purchaseorder"),
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
    path("addestimate/", views.addestimate, name="addestimate"),
    path("creditnote/", views.creditnote, name="creditnote"),
    path('addreceipts/', views.addreceipts, name='addreceipts'),
    path('addpaymentsout/', views.addpaymentsout, name='addpaymentsout'),
    path('addvendorinvoice/', views.addvendorinvoice, name='addvendorinvoice'),
    path('claimapproval/', views.claimapproval, name='claimapproval'),
    path('claimrequest/', views.claimrequest, name='claimrequest'),
    path('materialinward/', views.materialinward, name='materialinward'),
    path('addmaterialinward/', views.addmaterialinward, name='addmaterialinward'),
    path("addsalesinvoice/", views.addsalesinvoice, name="addsalesinvoice"),
    path("addsalesorders/", views.addsalesorders, name="addsalesorders"),
    path("taxmaster/", views.taxmaster, name="taxmaster"),
    path("user/", views.user, name="user"),
    path("addpurchaseorder/", views.addpurchaseorder, name="addpurchaseorder"),
    path("addpurchasereturn/", views.addpurchasereturn, name="addpurchasereturn"),
    path('addclaimrequest/', views.addclaimrequest, name='addclaimrequest'),
    path("report/", views.report, name="report"),
    path("salesdashboard/", views.salesdashboard, name="salesdashboard"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('groups/edit/<str:group_type>/<str:group_code>/', views.edit_group, name='edit_group'),
    path('groups/delete/<str:group_type>/<str:group_code>/', views.delete_group, name='delete_group'),
    path('edit-customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('edit-supplier/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('delete-supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('edit_materialinward/<int:inward_id>/', views.edit_materialinward, name='edit_materialinward'),
    path('delete_materialinward/<int:inward_id>/', views.delete_materialinward, name='delete_materialinward'),
    path('edit-tax/<int:tax_id>/', views.edit_tax, name='edit_tax'),  
    path('delete-tax/<int:tax_id>/', views.delete_tax, name='delete_tax'),
    path('material/edit/<str:category>/', views.edit_material, name='edit_material'),
    path('material/delete/<str:category>/', views.delete_material, name='delete_material'),
    path('create-hsn-code/', views.create_hsn_code, name='create_hsn_code'),
    path('select-hsn-code/', views.select_hsn_code, name='select_hsn_code'),
    # path('search-hsn-codes/', views.search_hsn_codes, name='search_hsn_codes'),
    path('get_hsn_suggestions/', views.get_hsn_suggestions, name='get_hsn_suggestions'),
    path('api/material-autocomplete/', views.material_autocomplete, name='material_autocomplete'),
    path('api/vendor-autocomplete/', views.vendor_autocomplete, name='vendor_autocomplete'),
    path('api/material-suggestions/', views.material_suggestions, name='material_suggestions'),
    path('api/material-name-suggestions/', views.material_name_suggestions, name='material_name_suggestions'),
    path('edit-price/<str:material_code>/', views.edit_price, name='edit_price'),
    path('delete-price/<str:material_code>/', views.delete_price, name='delete_price'),
    path('api/get-hsn-codes-with-taxes/', views.get_hsn_codes_with_taxes, name='get_hsn_codes_with_taxes'),
     # API Endpoints
    path('api/materialestimate-autocomplete/', views.materialestimate_autocomplete, name='materialestimate_autocomplete'),
    path('api/get-tax-rates/', views.get_tax_rates, name='get_tax_rates'),
    path('api/get-customer-address/', views.get_customer_address, name='get_customer_address'),
    path('api/customer-autocomplete/', views.customer_autocomplete, name='customer_autocomplete'),
    path('api/warehouse-autocomplete/', views.warehouse_autocomplete, name='warehouse_autocomplete'),
    path('claim-request/delete/<int:claim_id>/', views.delete_claim_request, name='delete_claim_request'),
    # Claim request pages
    path('claimrequest/', views.claimrequest, name='claimrequest'),
    path('addclaimrequest/', views.addclaimrequest, name='addclaimrequest'),
    # In your urlpatterns, add this line:
   # path('claim-request/edit/<int:claim_id>/', views.edit_claim_request, name='edit_claim_request'),
    #path('claim-request/delete/<int:claim_id>/', views.delete_claim_request, name='delete_claim_request'),
    # In your urls.py, make sure you have:
    path('addclaimrequest/', views.add_claim_request, name='addclaimrequest'),
     # Add this line for edit claim
    # Claim request pages
    path('claimrequest/', views.claimrequest, name='claimrequest'),
    path('addclaimrequest/', views.addclaimrequest, name='addclaimrequest'),
    # Add this line for delete claim
    path('delete-claim/<int:claim_id>/', views.delete_claim_request, name='delete_claim_request'),
    # Claim request APIs
    path('api/claim-requests/', views.claim_requests_api, name='claim_requests_api'),
    path('api/claim-requests/<int:claim_id>/', views.claim_request_detail_api, name='claim_request_detail_api'),
    path('api/claim-requests/<int:claim_id>/approval/', views.claim_approval_api, name='claim_approval_api'),
    # Claim approval URLs
    path('claim-details/<int:claim_id>/', views.get_claim_details, name='get_claim_details'),
    path('approve-claim/<int:claim_id>/', views.approve_claim, name='approve_claim'),
    path('reject-claim/<int:claim_id>/', views.reject_claim, name='reject_claim'),
    path('query-claim/<int:claim_id>/', views.query_claim, name='query_claim'),
    path('save-claim-approval/<int:claim_id>/', views.save_claim_approval, name='save_claim_approval'),
    # Add this for claim approval page view
    path('claim-approval/<int:claim_id>/', views.claim_approval_page, name='claim_approval_page'),
    path('claimapproval/', views.claimapproval, name='claimapproval'),
    # Add this for claim request list view
    path('claim-requests/', views.claim_request_list, name='claim_requests'),
    path('api/search-claims/', views.search_claims, name='search_claims'),
    path('api/claim-document-numbers/', views.get_claim_document_numbers, name='claim_document_numbers'),
    path('api/claim-requested-by/', views.get_claim_requested_by, name='claim_requested_by'),
    path('editwarehouse/<str:warehouse_code>/', views.edit_warehouse, name='edit_warehouse'),
    path('deletewarehouse/<str:warehouse_code>/', views.delete_warehouse, name='delete_warehouse'),
     path('create_estimate/', views.create_estimate, name='create_estimate'),
     # Add to your existing urlpatterns
path('api/get-estimate-suggestions/', views.get_estimate_suggestions, name='get_estimate_suggestions'),
path('api/get-customer-suggestions/', views.get_customer_suggestions, name='get_customer_suggestions'),
path('api/get-global-suggestions/', views.get_global_suggestions, name='get_global_suggestions'),
path('edit-estimate/<int:estimate_id>/', views.edit_estimate, name='edit_estimate'),
path('delete-estimate/<int:estimate_id>/', views.delete_estimate, name='delete_estimate'),
path('create_sales_order/', views.create_sales_order, name='create_sales_order'),
path('edit_sales_order/<int:order_id>/', views.edit_sales_order, name='edit_sales_order'),
path('delete_sales_order/<int:order_id>/', views.delete_sales_order, name='delete_sales_order'),
path('api/salesorder-suggestions/', views.get_sales_order_suggestions, name='salesorder_suggestions'),
path('api/salesorder-global-suggestions/', views.get_sales_order_global_suggestions, name='salesorder_global_suggestions'),
 path('create_sales_invoice/', views.create_sales_invoice, name='create_sales_invoice'),
    path('edit-sales-invoice/<int:invoice_id>/', views.edit_sales_invoice, name='edit_sales_invoice'),
    path('delete-sales-invoice/<int:invoice_id>/', views.delete_sales_invoice, name='delete_sales_invoice'),
    path('get-sales-invoice-suggestions/', views.get_sales_invoice_suggestions, name='get_sales_invoice_suggestions'),
    path('get-sales-invoice-global-suggestions/', views.get_sales_invoice_global_suggestions, name='get_sales_invoice_global_suggestions'),
     path('create_purchase_order/', views.create_purchase_order, name='create_purchase_order'),
    path('edit-purchase-order/<int:order_id>/', views.edit_purchase_order, name='edit_purchase_order'),
    path('delete-purchase-order/<int:order_id>/', views.delete_purchase_order, name='delete_purchase_order'),
    
    # Purchase Order API URLs (following sales order pattern)
    path('get-purchase-order-suggestions/', views.get_purchase_order_suggestions, name='get_purchase_order_suggestions'),
    path('get-purchase-order-global-suggestions/', views.get_purchase_order_global_suggestions, name='get_purchase_order_global_suggestions'),
    
    # Reuse existing APIs for vendor, warehouse, material, and tax
    # path('vendor-autocomplete/', views.vendor_autocomplete, name='vendor_autocomplete'),
    path('warehouse-autocomplete/', views.warehouse_autocomplete, name='warehouse_autocomplete'),
    path('material-autocomplete/', views.material_autocomplete, name='material_autocomplete'),
    path('get-tax-rates/', views.get_tax_rates, name='get_tax_rates'),
    path('api/vendor-details-po/', views.get_vendor_details_po, name='get_vendor_details_po'),

    path('api/vendor-search-po/', views.vendor_search_po, name='vendor_search_po'),


    # Purchase Order Search Suggestions APIs
    path('api/purchase-orders/suggestions/', views.purchase_order_suggestions, name='purchase_order_suggestions'),
    path('get_purchase_order_suggestions/', views.purchase_order_suggestions, name='get_purchase_order_suggestions'),
    path('get_global_suggestions/', views.get_global_suggestions, name='get_global_suggestions'),
    path('vendor_name_suggestions/', views.vendor_name_suggestions, name='vendor_name_suggestions'),
     path('create-vendor-invoice/', views.create_vendor_invoice, name='create_vendor_invoice'),
    path('edit-vendor-invoice/<int:invoice_id>/', views.edit_vendor_invoice, name='edit_vendor_invoice'),
    path('delete-vendor-invoice/<int:invoice_id>/', views.delete_vendor_invoice, name='delete_vendor_invoice'),
    

    # Vendor Invoice API URLs
    path('vendor-search/', views.vendor_search_autocomplete, name='vendor_search_autocomplete'),
    path('vendor-details/<int:vendor_id>/', views.get_vendor_details, name='get_vendor_details'),
    path('vendor-invoice-suggestions/', views.get_vendor_invoice_suggestions, name='get_vendor_invoice_suggestions'),
    path('vendor-invoice-global-suggestions/', views.get_vendor_invoice_global_suggestions, name='get_vendor_invoice_global_suggestions'),
        # AJAX API URLs for Vendor Payment
    path('get-vendor-due-amount/', views.get_vendor_due_amount, name='get_vendor_due_amount'),
    path('get-vendor-balance-after-payment/', views.get_vendor_balance_after_payment, name='get_vendor_balance_after_payment'),
      path('vendor_payment_suggestions/', views.vendor_payment_suggestions, name='vendor_payment_suggestions'),
    path('vendor-payment-details/', views.get_vendor_payment_details, name='vendor_payment_details'),
    path('vendor-payment-global-suggestions/', views.vendor_payment_global_suggestions, name='vendor_payment_global_suggestions'),
     path('get-vendor-documents/', views.get_vendor_documents, name='get_vendor_documents'),
      path('get-customer-outstanding/', views.get_customer_outstanding_amount, name='get_customer_outstanding'),
    path('get-customer-balance-after-receipt/', views.get_customer_balance_after_receipt, name='get_customer_balance_after_receipt'),
    path('customer-receipt-suggestions/', views.customer_receipt_suggestions, name='customer_receipt_suggestions'),
    path('get-customer-receipt-details/', views.get_customer_receipt_details, name='get_customer_receipt_details'),
    path('customer-receipt-global-suggestions/', views.customer_receipt_global_suggestions, name='customer_receipt_global_suggestions'),
    path('get-customer-invoices/', views.get_customer_invoices, name='get_customer_invoices'),
     path('view-receipt/<int:receipt_id>/', views.view_receipt, name='view_receipt'),
    path('edit-receipt/<int:receipt_id>/', views.edit_receipt, name='edit_receipt'),
    path('delete-receipt/<int:receipt_id>/', views.delete_receipt, name='delete_receipt'),
    path('home-search-suggestions/', views.home_search_suggestions, name='home_search_suggestions'),
      path('salesdashboard/', views.salesdashboard, name='salesdashboard'),
    # path('tracker/<int:tracker_id>/check-in-out/', views.check_in_out, name='check_in_out'),
     path('user/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('sales-invoice/<int:invoice_id>/pdf/', views.salesinvoicepdf, name='sales_invoice_pdf'),
    path('purchase-order-pdf/<int:po_id>/', views.purchaseorderpdf, name='purchase_order_pdf'),
    path('receipt-pdf/<int:receipt_id>/', views.receipt_pdf, name='receipt_pdf'),
    path('sales-order-pdf/<int:so_id>/', views.salesorder_pdf, name='salesorder_pdf'),
    path('grn-number-suggestions/', views.grn_number_suggestions, name='grn_number_suggestions'),
    path('batch-suggestions/', views.batch_suggestions, name='batch_suggestions'),
    path('api/warehouse-global-suggestions/', views.warehouse_global_suggestions, name='warehouse_global_suggestions'),
    path('checkin/', views.checkin_page, name='checkin_page'),
    path("checkout/", views.checkout, name="checkout"),
    path("update-assignment/<int:id>/", views.update_assignment, name="update_assignment"),
    path("api/dashboard-customer-search/", views.dashboard_customer_search, name="dashboard_customer_search"),
    path("api/update-customer/<int:tracker_id>/", views.update_customer_in_tracker, name="update_customer_in_tracker"),
    path("add-tracker/", views.add_tracker, name="add_tracker"),
    path("bulk-assign-trackers/", views.bulk_assign_trackers, name="bulk_assign_trackers")











  ] 