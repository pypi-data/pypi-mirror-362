from django.apps import AppConfig


class HidpWagtailConfig(AppConfig):
    name = "hidp_wagtail"
    label = "hidp_wagtail"
    verbose_name = "HIdP Wagtail"

    def ready(self):
        import hidp_wagtail.checks  # noqa: F401
