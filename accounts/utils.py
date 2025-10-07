from functools import wraps
import profile
from urllib import request
from django.http import HttpResponseForbidden




def require_role(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            role = getattr(getattr(request.user, 'profile', None), 'role', None)
            if role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Not allowed")
        return _wrapped
    return decorator



def org_queryset(qs, request):
    profile = getattr(request.user, 'profile', None)
    if profile and profile.organization:
        return qs.filter(organization=profile.organization)
    return qs.none()