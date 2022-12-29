import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.defaults import bad_request
from django_comments_ink import get_model, signed

from . import forget_me, remember_me
from .decorators import not_authenticated
from .forms import (
    CancelForm,
    LoginForm,
    ProfileForm,
    RegisterStep1Form,
    RegisterStep2Form,
    ResetPwdForm,
)
from .models import Confirmation
from .utils import (
    notify_emailaddr_change_confirmation,
    send_confirm_account_deletion_request,
    send_confirm_user_registration_request,
)

from .models import User
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from articles.models import Article

# Blog app imports
from users.forms import (
    UserUpdateForm,
    ProfileUpdateForm,
)


@not_authenticated
def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            if request.GET.get("next"):
                response = HttpResponseRedirect(request.GET.get("next"))
            else:
                response = HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            if form.cleaned_data.get("remember"):
                remember_me(response, form.user)
            login(request, form.user)
            return response
    return render(request, "users/login.html", {"form": form})


@not_authenticated
def user_register(request):
    form = RegisterStep1Form()
    if request.POST:
        form = RegisterStep1Form(request.POST)
        if form.is_valid():
            key = signed.dumps(
                request.POST,
                compress=True,
                extra_key=settings.COMMENTS_INK_SALT,
            )
            site = get_current_site(request)
            scheme = request.is_secure() and "https" or "http"
            send_confirm_user_registration_request(form, key, site, scheme)
            return render(
                request,
                "users/register_step_1_confirm.html",
                {"email": form.cleaned_data["email"]},
            )
    return render(request, "users/register_step_1.html", {"form": form})


@not_authenticated
def user_register_confirm(request, key):
    login_redirect = HttpResponseRedirect(settings.LOGIN_URL)
    if request.method == "GET":
        try:
            data = signed.loads(str(key), extra_key=settings.COMMENTS_INK_SALT)
            form = RegisterStep1Form(data)
            if form.is_valid():
                email = form.cleaned_data.get("email")
            else:
                return login_redirect
        except (ValueError, signed.BadSignature) as exc:
            return bad_request(request, exc)
        try:
            get_user_model().objects.get(email=email)
            return login_redirect
        except get_user_model().DoesNotExist as exc:
            get_user_model().objects.create(**form.cleaned_data)
    elif request.method == "POST":
        form = RegisterStep2Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = get_user_model().objects.get(email=email)
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            return render(
                request, "users/register_done.html", {"form": LoginForm()}
            )

    return render(
        request,
        "users/register_step_2.html",
        {"form": RegisterStep2Form(initial={"email": email})},
    )


@login_required
def user_logout(request):
    response = HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    forget_me(response)
    logout(request)
    return response


@login_required
def user_account(request):
    or_condition = Q(user=request.user) | Q(user_email=request.user.email)
    comments = get_model().objects.filter(or_condition).order_by("submit_date")
    return render(request, "users/account.html", {"comments": comments})


@login_required
def edit_profile(request):
    if request.POST:
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.name = form.cleaned_data["name"]
            request.user.url = form.cleaned_data["url"]
            request.user.save()

            if form.cleaned_data["email"] != request.user.email:
                # The user wants to change the registered email
                # address, so send a confirmation request.
                key = signed.dumps(
                    form.cleaned_data["email"],
                    compress=True,
                    extra_key=settings.COMMENTS_INK_SALT,
                )
                site = get_current_site(request)
                scheme = request.is_secure() and "https" or "http"
                notify_emailaddr_change_confirmation(
                    key, request.user, form.cleaned_data["email"], site, scheme
                )
                messages.info(
                    request,
                    (
                        "A confirmation request has been sent"
                        " to your new email address."
                    ),
                )
                return HttpResponseRedirect(reverse("edit-profile"))
            else:
                messages.success(request, "Your personal data has been saved.")
    else:
        form = ProfileForm(user=request.user)

    return render(request, "users/edit_account.html", {"form": form})


@login_required
def confirm_change_email(request, key):
    try:
        email = signed.loads(key, extra_key=settings.COMMENTS_INK_SALT)
    except (ValueError, signed.BadSignature) as exc:
        return bad_request(request, exc)

    try:
        confirm = Confirmation.objects.get(
            email=request.user.email, purpose="E"
        )
    except Confirmation.DoesNotExist as exc:
        return HttpResponseRedirect(reverse("logout"))

    if confirm.key != email:
        return render(request, "users/change_email_error.html")

    request.user.email = email
    request.user.save()
    confirm.delete()
    messages.success(request, "Your email address has been changed.")
    return HttpResponseRedirect(reverse("edit-profile"))


@login_required
def edit_password(request):
    if request.POST:
        form = ResetPwdForm(data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data.get("pwd1"))
            request.user.save()
            messages.success(request, _("Successfully changed your password."))
            messages.info(
                request, _("You need to login again with your new password.")
            )
    else:
        form = ResetPwdForm()

    return render(request, "users/change_password.html", {"form": form})


@login_required
def user_delete(request):
    if request.POST:
        form = CancelForm(data=request.POST)
        if form.is_valid():
            post_dict = dict.copy(request.POST)
            post_dict.pop("csrfmiddlewaretoken")
            post_dict["noise"] = "".join(
                [
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(random.randint(24, 32))
                ]
            )
            post_dict["email"] = request.user.email
            key = signed.dumps(
                post_dict, compress=True, extra_key=settings.COMMENTS_INK_SALT
            )
            site = get_current_site(request)
            send_confirm_account_deletion_request(request.user, key, site)
            return render(request, "users/delete_step_1_confirm.html")
    else:
        form = CancelForm()

    return render(request, "users/delete_step_1.html", {"form": form})


@login_required
def user_delete_confirm(request, key):
    try:
        data = signed.loads(str(key), extra_key=settings.COMMENTS_INK_SALT)
        if data.get("email") != request.user.email:
            raise ValueError(
                "The deletion request was generated for %s, "
                "but the current active account email is %s.?!?",
                *(data.get("email"), request.user.email)
            )
    except (ValueError, signed.BadSignature) as exc:
        return bad_request(request, exc)
    # TODO: Delete the user taking into account the 'anonymize'
    #       field provided within the data dict.
    print("TODO: Now I can delete the account.")
    return user_logout(request)


class DashboardHomeView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'author/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        articles_list = Article.objects.filter(author=request.user)

        total_articles_written = len(articles_list)
        total_articles_published = len(articles_list.filter(status='published'))
        total_articles_views = sum(article.views for article in articles_list)

        recent_published_articles_list = articles_list.filter(status='published').order_by("-date_published")[:5]

        self.context['total_articles_written'] = total_articles_written
        self.context['total_articles_published'] = total_articles_published
        self.context['total_articles_views'] = total_articles_views
        self.context['recent_published_articles_list'] = recent_published_articles_list

        return render(request, self.template_name, self.context)


class AuthorProfileView(LoginRequiredMixin, View):
    """
    Displays author profile details
    """
    template_name = "author/author_profile_detail.html"
    context_object = {}

    def get(self, request):
        author = User.objects.get(name=request.user)

        self.context_object['author_profile_details'] = author
        return render(request, self.template_name, self.context_object)


class AuthorProfileUpdateView(LoginRequiredMixin, View):
    """
     Updates author profile details
    """
    template_name = 'author/author_profile_update.html'
    context_object = {}

    def get(self, request):
        user_form = UserUpdateForm(instance=self.request.user)
        profile_form = ProfileUpdateForm(instance=self.request.user.profile)

        self.context_object['user_form'] = user_form
        self.context_object['profile_form'] = profile_form

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(data=request.POST, instance=self.request.user)
        profile_form = ProfileUpdateForm(data=request.POST, files=request.FILES,
                                         instance=self.request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            messages.success(request, f'Your account has successfully '
                                      f'been updated!')
            return redirect('author_profile_details')

        else:
            user_form = UserUpdateForm(instance=self.request.user)
            profile_form = ProfileUpdateForm(instance=self.request.user.profile)

            self.context_object['user_form'] = user_form
            self.context_object['profile_form'] = profile_form

            messages.error(request, f'Invalid data. Please provide valid data.')
            return render(request, self.template_name, self.context_object)


class AuthorWrittenArticlesView(LoginRequiredMixin, View):
    """
       Displays all articles written by an author.
    """

    def get(self, request):
        """
           Returns all articles written by an author.
        """
        template_name = 'author/author_written_article_list.html'
        context_object = {}

        written_articles = Article.objects.filter(author=request.user.id).order_by('-date_created')
        total_articles_written = len(written_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(written_articles, 5)
        try:
            written_articles_list = paginator.page(page)
        except PageNotAnInteger:
            written_articles_list = paginator.page(1)
        except EmptyPage:
            written_articles_list = paginator.page(paginator.num_pages)

        context_object['written_articles_list'] = written_articles_list
        context_object['total_articles_written'] = total_articles_written

        return render(request, template_name, context_object)