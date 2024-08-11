from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

from django.shortcuts import redirect
from django.urls import reverse

class RedirectAnonymousUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the URLs that should be exempt from redirection
        exempt_urls = [
            reverse('account_login'),
            reverse('account_signup'),
            reverse('user_signup'),
            reverse('account_reset_password'),
            reverse('account_reset_password_done'),
            # reverse('account_reset_password_confirm', kwargs={'uidb64': 'dummy', 'token': 'dummy-token'}),
            reverse('account_inactive'),  # Typically used for inactive accounts
        ]

        # Avoid redirecting if the user is on an exempt URL
        if request.user.is_anonymous and request.path not in exempt_urls:
            return redirect(reverse('account_login'))

        response = self.get_response(request)
        return response

