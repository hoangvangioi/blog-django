import re

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm

from .models import Confirmation, User, Profile


# ---------------------------------------------------------------------
# Login form.

confirm_pending_msg = _(
    "Your registration process is not finished yet, you  have to confirm your e-Mail address. Check the e-Mail message we already sent you."
)
usr_not_active_msg = _("This user account is not active.")
usr_not_auth_msg = _(
    "Enter a correct e-Mail address and password. Note that both fields are case-sensitive."
)


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={"tabindex": 1, 'placeholder': 'e.g: john@gmail.com ', 'class': 'bg-gray-200 border rounded text-xs font-medium leading-none placeholder-gray-800 text-gray-800 py-3 w-full pl-3 mt-2'}))
    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={"tabindex": 2, 'placeholder': ' ******** ', 'class': 'bg-gray-200 border rounded text-xs font-medium leading-none text-gray-800 py-3 w-full pl-3 mt-2'}))
    remember = forms.BooleanField(
        widget=forms.CheckboxInput, required=False, label=_("Remember me")
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['password'].widget.attrs['type'] = 'password'

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(self.request, email=email, password=password)
            if not user:
                raise forms.ValidationError(usr_not_auth_msg)
            else:
                self.user = user
                try:
                    confirmation = Confirmation.objects.get(email=email)
                except Confirmation.DoesNotExist:
                    if not user.is_active:
                        raise forms.ValidationError(usr_not_active_msg)
                else:
                    if not user.is_active:
                        raise forms.ValidationError(confirm_pending_msg)
                    else:
                        confirmation.delete()

        return self.cleaned_data


# ---------------------------------------------------------------------
# Register forms:
# * 1st step: Provide email, name and URL.
# * ... Once email is confirmed ...
# * 2nd step: Provide a password for your account.


class RegisterStep1Form(forms.Form):
    email = forms.EmailField(
        required=True,
        label=_("Email"),
        widget=forms.EmailInput(attrs={"tabindex": 1, 'placeholder': 'e.g: john@gmail.com ', 'type':'email', 'class': 'bg-gray-200 border rounded text-xs font-medium leading-none placeholder-gray-800 text-gray-800 py-3 w-full pl-3 mt-2'}))
    name = forms.CharField(
        required=True,
        label=_("Name"),
        max_length=150,
        widget=forms.TextInput(attrs={"size": 30, "tabindex": 2, 'placeholder': 'Full Name ', 'class': 'bg-gray-200 border rounded text-xs font-medium leading-none text-gray-800 py-3 w-full pl-3 mt-2'}),
    )

    def clean_email(self):
        if "email" in self.cleaned_data:
            email = self.cleaned_data["email"].lower()
            try:
                get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                return email
            else:
                raise forms.ValidationError(
                    _("This email address is already registered.")
                )

    def clean_name(self):
        if "name" in self.cleaned_data:
            if (
                re.search(r"^[\W]+", self.cleaned_data["name"]) != None
                or len(self.cleaned_data["name"]) < 5
            ):
                raise forms.ValidationError(
                    _("Please, provide a name with at least 5 characters.")
                )
            return self.cleaned_data["name"]


class RegisterStep2Form(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    password = forms.CharField(
        label=_("Create Password"),
        widget=forms.PasswordInput(
            attrs={"size": 30, 'type': 'password', "autocomplete": "new-password", 'class': 'w-full p-3 mt-4 border border-gray-300 rounded outline-none focus:bg-gray-50'}
        ),
    )

    def clean_password(self):
        if "password" in self.cleaned_data:
            if len(self.cleaned_data["password"]) < 6:
                raise forms.ValidationError(
                    _(
                        "For your account's security "
                        "please, provide a longer "
                        "password."
                    )
                )
            return self.cleaned_data["password"]


# ---------------------------------------------------------------------
# Change email address form.

email_already_registered = "This email address is already registered."
too_many_attempts = (
    "Please, wait 24 hours to request another email address change."
)
profile_did_not_change = "Data did not change."


class ProfileForm(forms.Form):
    email = forms.CharField(required=True, 
    widget=forms.EmailInput(attrs={'class': 'bordder-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none'}),
    )
    name = forms.CharField(max_length=150, required=False, label=_("Name"), 
    widget=forms.TextInput(attrs={'class': 'bordder-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none'}),)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        if self.user:
            kwargs["initial"] = {
                "email": self.user.email,
                "name": self.user.name,
            }
        super().__init__(*args, **kwargs)

    def clean_email(self):
        # Check if strip is necessary.
        email = self.cleaned_data["email"].strip()
        if self.user and self.user.email == email:
            return email

        try:
            if User.objects.filter(email=email).count():
                raise forms.ValidationError(email_already_registered)

            # If there is already an email change confirmation
            # for this user, the update the confirmation.
            confirm = Confirmation.objects.get(email=self.user.email)
            if not confirm.is_out_of_date() and confirm.notifications < 3:
                confirm.key = email
                confirm.notifications += 1
                confirm.save()
                return email

            elif confirm.is_out_of_date():
                confirm.delete()
                Confirmation.objects.create(
                    email=self.user.email, key=email, purpose="E"
                )  # Change email.
                return email

            else:
                raise forms.ValidationError(too_many_attempts)

        except Confirmation.DoesNotExist as exc:
            Confirmation.objects.create(
                email=self.user.email, key=email, purpose="E"
            )  # Change email.
            return email

    def clean(self):
        email = self.cleaned_data["email"].strip()
        name = self.cleaned_data["name"].strip()

        if (
            self.user
            and email == self.user.email
            and name == self.user.name
        ):
            raise forms.ValidationError(profile_did_not_change)

        return self.cleaned_data


# --------------------------------------------------------------------
# Change password form.


class ResetPwdForm(forms.Form):
    """Reset Password Form."""

    pwd1 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={"size": 26, "tabindex": 1, 'class': 'bordder-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none'}),
        label=_("Type a New Password"),
    )
    pwd2 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={"size": 26, "tabindex": 2, 'class': 'bordder-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none'}),
        label=_("Confirm the Password"),
    )

    def clean(self):
        pwd1 = self.cleaned_data.get("pwd1")
        pwd2 = self.cleaned_data.get("pwd2")

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError(
                _("Please, type the same password in both fields.")
            )
        return self.cleaned_data


# ---------------------------------------------------------------------
# Change password form.


ANONYMIZE_CHOICES = (
    ("Y", _("Anonymize my contributions.")),
    ("N", _("Keep my name in my contributions.")),
)


class CancelForm(forms.Form):
    """Account cancelation Form."""

    anonymize = forms.ChoiceField(
        choices=ANONYMIZE_CHOICES,
        initial="Y",
        widget=forms.RadioSelect(),
        label=_("About my contributions"),
    )
    cancel = forms.BooleanField(
        label=_("Yes, I want to cancel my account."), required=False
    )

    def clean_cancel(self):
        if not self.cleaned_data["cancel"]:
            raise forms.ValidationError(
                _("You must confirm that you want to cancel your account")
            )
        return self.cleaned_data["cancel"]


class UserUpdateForm(forms.ModelForm):
    """
        Creates form for user to update their account.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                                                     'class': "pl-3 py-3 w-full text-sm focus:outline-none placeholder-gray-500 rounded bg-transparent text-gray-600 dark:text-gray-400",
                                                    }
                                                ),
                                            )

    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {

            'name': forms.TextInput(attrs={
                'class': "border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm bg-transparent rounded text-sm focus:outline-none focus:border-indigo-700 placeholder-gray-500 text-gray-600 dark:text-gray-400",
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    """
       Creates form for user to update their Profile.
    """
    class Meta:
        model = Profile
        fields = ['avatar', 'job_title', 'bio', 'address',
                  'twitter_url', 'github_url',
                  'facebook_url', 'instagram_url']

        widgets = {

            'job_title': forms.TextInput(attrs={
                'name': "job-title",
                'class': "border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded bg-transparent text-sm focus:outline-none focus:border-indigo-700 placeholder-gray-500 text-gray-600 dark:text-gray-400",
                'id': "job-title"
            }),

            'bio': forms.Textarea(attrs={
                'name': "bio",
                'class': "bg-transparent border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded text-sm focus:outline-none focus:border-indigo-700 resize-none placeholder-gray-500 text-gray-600 dark:text-gray-400",
                'id': "bio", "rows": "6",
            }),

            'address': forms.TextInput(attrs={
                'name': "address",
                'class': "border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded bg-transparent text-sm focus:outline-none focus:border-indigo-700 placeholder-gray-500 text-gray-600 dark:text-gray-400",
                'id': "address"
            }),

            'avatar': forms.FileInput(attrs={
                "class": "hidden",
                "type": "file",
                "id": "profileImage",
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields['facebook_url'].widget.attrs['class'] = 'border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded bg-transparent text-sm focus:outline-none focus:border-indigo-700 placeholder-gray-500 text-gray-600 dark:text-gray-400'
            self.fields['twitter_url'].widget.attrs['class'] = 'border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded bg-transparent text-sm focus:outline-none focus:border-indigo-700 placeholder-gray-500 text-gray-600 dark:text-gray-400'
            self.fields['instagram_url'].widget.attrs['class'] = 'border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded bg-transparent text-sm focus:outline-none focus:border-indigo-700 placeholder-gray-500 text-gray-600 dark:text-gray-400'
            self.fields['github_url'].widget.attrs['class'] = 'border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded bg-transparent text-sm focus:outline-none focus:border-indigo-700 placeholder-gray-500 text-gray-600 dark:text-gray-400'