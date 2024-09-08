from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

class ApprovalRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        if (request.path.startswith('/admin/')
            or request.path == reverse('approval_pending')
            or request.path in [reverse('login'), reverse('logout')]):
            return response
        
        
        if (request.user.is_authenticated 
        and not request.user.is_staff 
        and not request.user.is_superuser):
            tenant = getattr(request.user, 'tenant', None)
            if tenant and not tenant.approved:
                return HttpResponseRedirect(reverse('approval_pending'))
        return response