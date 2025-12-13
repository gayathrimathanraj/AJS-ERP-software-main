# ajserp/utils.py

from django.shortcuts import redirect
from .models import PagePermission
import requests
from django.conf import settings

# ----------------------------------------------------------
# MODULE → SUBMENU PERMISSION STRUCTURE
# ----------------------------------------------------------

modules = [

    {
        "key": "inventory",
        "label": "Inventory",
        "submenus": [
            {"key": "material", "label": "Material"},
            {"key": "material_inward", "label": "Material Inward"},
            {"key": "warehouse", "label": "Warehouse"},
            {"key": "price_list", "label": "Price List"},
        ]
    },

    {
        "key": "parties",
        "label": "Parties",
        "submenus": [
            {"key": "customer", "label": "Customer"},
            {"key": "supplier", "label": "Supplier"},
            {"key": "group", "label": "Group"},
        ]
    },

    {
        "key": "sales",
        "label": "Sales",
        "submenus": [
            {"key": "estimate", "label": "Estimate"},
            {"key": "sales_order", "label": "Sales Order"},
            {"key": "sales_invoice", "label": "Sales Invoice"},
        ]
    },

    {
        "key": "purchase",
        "label": "Purchase",
        "submenus": [
            {"key": "purchase_order", "label": "Purchase Order"},
            {"key": "purchase_return", "label": "Purchase Return"},
        ]
    },

    {
        "key": "finance",
        "label": "Finance",
        "submenus": [
            {"key": "expenses", "label": "Expenses"},
            {"key": "receipt", "label": "Receipt"},
            {"key": "payment", "label": "Vendor Payment"},
            {"key": "vendor_invoice", "label": "Vendor Invoice"},
        ]
    },

    {
        "key": "claim",
        "label": "Claim",
        "submenus": [
            {"key": "claim_request", "label": "Claim Request"},
            {"key": "claim_approval", "label": "Claim Approval"},
        ]
    },

    {
        "key": "tax_master",
        "label": "Tax Master",
        "submenus": [
            {"key": "tax_master_sub", "label": "Tax Master"},
        ]
    },

    {
        "key": "user",
        "label": "User",
        "submenus": [
            {"key": "add_user", "label": "Add User"},
        ]
    },
]

# ----------------------------------------------------------
# DECORATOR → CHECK SUBMENU PERMISSION
# ----------------------------------------------------------
def submenu_required(module, submenu):
    key = f"{module}__{submenu}"

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if getattr(request.user, "role", "") == "admin":
                return view_func(request, *args, **kwargs)

            if PagePermission.objects.filter(
                user=request.user,
                page_name=key,
            ).exists():
                return view_func(request, *args, **kwargs)

            return redirect("ajserp:not_allowed")
        return wrapper
    return decorator


def require_permission(module, submenu, action):
    """
    Usage: @require_permission("inventory", "material", "view")
    """
    key = f"{module}__{submenu}__{action}"

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            # Admin → full access
            if getattr(request.user, "role", "") == "admin":
                return view_func(request, *args, **kwargs)

            # Normal user → check permission row exists
            if PagePermission.objects.filter(
                user=request.user,
                page_name=key,
            ).exists():
                return view_func(request, *args, **kwargs)

            return redirect("ajserp:not_allowed")

        return wrapper

    return decorator  

def send_fast2sms(number, message):
    """
    Simple Fast2SMS integration.
    `number` : mobile number as string (10-digit or with 91)
    `message`: sms text
    """
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "q",             # quick route for testing
        "message": message,
        "language": "english",
        "numbers": number,
    }

    headers = {
        "authorization": settings.FAST2SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        return response.json()
    except Exception as e:
        print("Fast2SMS Error:", e)
        return None
