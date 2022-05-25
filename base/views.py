from django.shortcuts import redirect, render
from django.template import RequestContext


# def handler404(request, exception,):
#     return render(request, '404.html')


# def handler500(request, *args, **argv):
#     return render(request, '404.html', status=500)


# def csrf_failure(request, reason=""):
#     return render(request, '404.html', status=403)

def error(request):
    render(request, '404.html')


def handler404(request, exception=None):
    response = render(
        '404.html',
        context_instance=RequestContext(request)
        )
    response.status_code = 404

    return redirect('/error')


# def handler500(exception=None):
#     return redirect('/error')


# def csrf_failure(exception=None, reason=""):
#     return redirect('/error')


# def handler400(exception=None):
#     return redirect('/error')

# def handler404(request, *args, **argv):
#     response = render('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response


# from django.shortcuts import render
# from django.template import RequestContext

# # HTTP Error 400
# def bad_request(request):
#     response = render(
#         '400.html',
#         context_instance=RequestContext(request)
#         )

#     response.status_code = 400

#     return response




# def custom_page_not_found_view(request, exception):
#     return render(request, "404.html", {})

# def custom_error_view(request, exception=None):
#     return render(request, "500.html", {})

# def custom_permission_denied_view(request, exception=None):
#     return render(request, "403.html", {})

# def custom_bad_request_view(request, exception=None):
#     return render(request, "400.html", {})