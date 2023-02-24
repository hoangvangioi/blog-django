from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect


def not_authenticated(func=None):
    """
    Decorator that redirect user to its account settings entry if it is
    already logged in.
    """

    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return func(request, *args, **kwargs)

    return decorated


def superuser_required(function):
	def wrap(request, *args, **kwargs):
		if request.user.is_superuser:
			return function(request, *args, **kwargs)
		else:
			return render(request, '404.html')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap