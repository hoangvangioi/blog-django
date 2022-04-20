from django.shortcuts import render


def error(request, exception,):
    return render(request, '404.html')


def handler500(request, *args, **argv):
    return render(request, '404.html', status=500)

def handler403(request, *args, **argv):
    return render(request, '404.html', status=403)


def csrf_failure(request, reason=""):
    return render(request, '404.html', status=403)


def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)

def error_500(request):
        data = {}
        return render(request,'404.html', data)