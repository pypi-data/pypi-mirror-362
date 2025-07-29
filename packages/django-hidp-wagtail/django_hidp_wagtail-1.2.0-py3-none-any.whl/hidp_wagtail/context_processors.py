from hidp.utils import get_account_management_links


def account_management_links(request):
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        return {"account_management_links": get_account_management_links(user)}
    return {}
