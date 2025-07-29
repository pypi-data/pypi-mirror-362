from hidp.otp.middleware import OTPMiddlewareBase

from django.urls import reverse


class OTPRequiredForWagtailAdminMiddleware(OTPMiddlewareBase):
    """
    Middleware that requires OTP verification for users accessing the Wagtail admin.

    - Applies only to requests to the Wagtail admin interface.
    - Redirects to OTP verification or setup if not verified.
    - Ensures user has Wagtail admin access (wagtailadmin.access_admin).
    """

    def user_needs_verification(self, user):
        """
        Require OTP verification only for users with Wagtail admin access.
        """
        return user.has_perm("wagtailadmin.access_admin")

    def request_needs_verification(self, request, view_func):
        """
        Apply OTP checks only when accessing the Wagtail admin interface.
        """
        if request.path.startswith(reverse("wagtailadmin_home")):
            return super().request_needs_verification(request, view_func)

        return False
