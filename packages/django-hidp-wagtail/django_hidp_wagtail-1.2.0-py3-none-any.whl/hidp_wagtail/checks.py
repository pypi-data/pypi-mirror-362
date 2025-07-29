from django.core.checks import Error, register
from django.conf import settings

from hidp.config.checks import Tags


@register(Tags.settings)
def check_wagtailadmin_login_url(app_configs, **kwargs):
    """
    Custom system check to ensure that the 'WAGTAILADMIN_LOGIN_URL' setting is configured.

    This check verifies that the 'WAGTAILADMIN_LOGIN_URL' setting is present in the Django settings.
    If the setting is not found, it raises an error with a hint on how to set it.
    """
    errors = []
    if not hasattr(settings, "WAGTAILADMIN_LOGIN_URL"):
        errors.append(
            Error(
                "The setting 'WAGTAILADMIN_LOGIN_URL' is not set.",
                hint="Set this to the URL of HIdP's login view (e.g. 'hidp_accounts:login').",
                id="hidp_wagtail.E001",
            )
        )
    return errors


@register(Tags.settings)
def check_account_management_links_context_processor(app_configs, **kwargs):
    """
    Custom system check to ensure that the 'account_management_links' context processor is configured.

    This check verifies that the 'account_management_links' context processor is present in the Django settings.
    If the context processor is not found, it raises an error with a hint on how to set it.
    """
    errors = []
    if all(
        "hidp_wagtail.context_processors.account_management_links"
        not in template_engine["OPTIONS"]["context_processors"]
        for template_engine in settings.TEMPLATES
    ):
        errors.append(
            Error(
                "The context processor 'hidp_wagtail.context_processors.account_management_links' is not set.",
                hint="Add this to your TEMPLATES['OPTIONS']['context_processors'] setting.",
                id="hidp_wagtail.E002",
            )
        )
    return errors
