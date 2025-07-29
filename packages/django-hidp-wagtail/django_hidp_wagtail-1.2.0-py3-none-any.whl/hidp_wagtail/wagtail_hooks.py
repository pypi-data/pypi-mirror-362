from wagtail import hooks
from django.urls import reverse
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_custom_menu_item():
    return MenuItem(
        "Account security",
        reverse("hidp_account_management:manage_account"),
        icon_name="password",
        order=1000,
    )
