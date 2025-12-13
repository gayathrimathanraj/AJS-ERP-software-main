print("✅✅✅ signals.py LOADED SUCCESSFULLY ✅✅✅")

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SalesOrder
from .utils import send_fast2sms   # ✅ CORRECT IMPORT
from .models import SalesInvoice

@receiver(post_save, sender=SalesOrder)
def auto_send_sales_order_sms(sender, instance, created, **kwargs):
    if created:   # ✅ Only when order is NEW

        customer = instance.customer
        mobile = customer.contact_number   # ✅ Your correct field

        if not mobile:
            print("❌ SMS NOT SENT: Customer mobile number missing")
            return

        message = (
            f"Dear {customer.customer_name}, "
            f"your Sales Order {instance.order_number} dated {instance.date}  "
            f"for amount ₹{instance.grand_total} has been created. "
            f"Thank you!"
        )

        result = send_fast2sms(str(mobile), message)

        if result and result.get("return") is True:
            print(f"✅ AUTO SMS SENT to {mobile}")
        else:
            print("❌ AUTO SMS FAILED:", result)

@receiver(post_save, sender=SalesInvoice)
def auto_send_invoice_sms(sender, instance, created, **kwargs):
    """
    Auto-send SMS when a SalesInvoice is created.
    If you prefer to send only when invoice is 'issued', adjust logic below.
    """
    # Only on creation (not every save)
    if not created:
        return

    try:
        customer = instance.customer
        mobile = getattr(customer, "contact_number", None)  # robust access

        if not mobile:
            print("❌ INVOICE SMS NOT SENT: Customer mobile number missing")
            return

        # Build message (customize as needed)
        message = (
            f"Dear {customer.customer_name}, "
            f"your Invoice {instance.invoice_number} dated {instance.date.strftime('%d-%m-%Y')} "
            f"for amount ₹{instance.grand_total:.2f} has been issued. Thank you!"
        )

        result = send_fast2sms(str(mobile), message)

        if result and result.get("return") is True:
            print(f"✅ AUTO INVOICE SMS SENT to {mobile}")
        else:
            # Print response to help debug (wallet / auth / format issues)
            print("❌ AUTO INVOICE SMS FAILED:", result)

    except Exception as e:
        # Avoid crashing save flow — log for debugging
        print("❌ Exception in auto_send_invoice_sms:", e)