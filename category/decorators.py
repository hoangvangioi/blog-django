from django.shortcuts import render

def superuser_required(function):
	def wrap(request, *args, **kwargs):
		if request.user.is_superuser:
			return function(request, *args, **kwargs)
		else:
			return render(request, '404.html')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap