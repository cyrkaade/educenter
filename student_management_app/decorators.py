from django.http import HttpResponseRedirect
from datetime import date
from .models import Students
from django.contrib import messages
from django.http import HttpResponseForbidden

def require_subscription(view_func):
    def _wrapped_view(request, *args, **kwargs):
        student = Students.objects.get(admin=request.user)
        if student.has_paid():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You need an active subscription to access this page.')

    return _wrapped_view