from .models import PagePermission

def user_permissions(request):
    if not request.user.is_authenticated:
        return {"user_permissions": []}

    # ✅ Admin gets everything
    if getattr(request.user, "role", None) == "admin":
        return {"user_permissions": "ALL"}

    permissions = list(
        PagePermission.objects.filter(user=request.user)
        .values_list("page_name", flat=True)
    )

    return {"user_permissions": permissions}
