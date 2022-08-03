from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DetailView, FormView,
                                  RedirectView, TemplateView, UpdateView)

from accounts.forms import ProfileForm, SignUpForm
from accounts.models import Account, Profile

from .token import token_generator


def send_active_email(user, request):
    current_site = get_current_site(request)
    email_subject = _('Please activate your account')
    email_body = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        # from_email=settings.DEFAULT_FROM_USER,
        to=[user.email],
    )
    email.send(fail_silently=False)


class SignUpView(FormView):
    form_class = SignUpForm 
    template_name = 'accounts/register.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            send_active_email(user, request)

            messages.success(request, f'A user verification link has been send to confirm your registration.')
            return render(request, 'accounts/register.html')
        # else:
        #     user_form = UserForm()
        #     profile_form = UserProfileInfoForm()

        return render(request, self.template_name, {'form': form})

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(SignUpView, self).get(*args, **kwargs)


class ActivateView(RedirectView):
    # Custom get method
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, _('Congratulations! Your account is activated.'))
            return redirect('post')
            # return super().get(request, uidb64, token)
        else:
            messages.error(request, _('Invalid activation link!'))
            return redirect('register')
            # return render(request, 'users/activate_account_invalid.html')


# class LogInView(FormView):
#     form_class = LoginForm 
#     template_name = 'accounts/login.html'

#     def form_valid(self, form):
#         #get the email and password
#         email = self.request.POST['email']
#         password = self.request.POST['password']
#         #authenticate user then login
#         user = auth.authenticate(email=email, password=password)
#         login(self.request, user)
#         return redirect('post')

    # def form_valid(self, form):
    #     # login(self.request, form.get_user())
    #     # return super(LogInView, self).form_valid(form)

    #     email = self.request.POST['email']
    #     password = self.request.POST['password']
    #     user = auth.authenticate(email=email, password=password)
    #     if user is not None:
    #         auth.login(self.request, user)
    #         messages.success(self.request, _('You are now logged in.'))
    #         url = self.request.META.get('HTTP_REFERER')
    #         try:
    #             query = requests.utils.urlparse(url).query
    #             params = dict(x.split('=') for x in query.split('&'))
    #             if 'next' in params:
    #                 nextPage = params['next']
    #                 return redirect(nextPage)                
    #         except:
    #             return redirect('post')
    #     else:
    #         messages.error(self.request, _('Invalid credentials!'))
    #         return redirect('login')


class ProfileDetailView(DetailView):
    model = Profile
    queryset = Profile.objects.all()
    context_object_name = 'profile'
    template_name = "accounts/profile.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/edit_profile.html"
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        profile = form.save()
        profile.user.first_name = form.cleaned_data.get('first_name')
        profile.user.last_name = form.cleaned_data.get('last_name')
        profile.user.save()
        return super().form_valid(form)
