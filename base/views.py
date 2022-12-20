from django.shortcuts import render


def handler400(request, *args, **kwargs):
    return render(request, '404.html', status=400)


def handler403(request, *args, **kwargs):
    return render(request, '403.html', status=403)


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, '404.html', status=500)