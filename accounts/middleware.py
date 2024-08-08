from django.shortcuts import redirect
from django.urls import reverse

class RedirectAnonymousUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_anonymous:
            return redirect(reverse('account_login'))
        response = self.get_response(request)
        return response