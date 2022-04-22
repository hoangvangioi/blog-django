from django import forms
from accounts.models import Account, Profile
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy


class RegisterForm(forms.ModelForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                            'class': 'form-control mb-2',
                                                            }))

    last_name = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control mb-2',
                                                              }))

    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control mb-2',
                                                           }))
    password = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control mb-2',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    confirm_password = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control mb-2',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
        
    
class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control mb-2',
                                                           }))
    password = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control mb-2',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
                                                                  
    class Meta:
        model = Account
        fields = ['email', 'password']


class PasswordChangeForm(SetPasswordForm):

    old_password = forms.CharField(
        label=("Mật khẩu cũ"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'


class SetPasswordForm(forms.Form):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
                                max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': "form-control col-sm-6",
                                    }))

    last_name = forms.CharField(required=False,
                                max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': "form-control col-sm-6",
                                    }))


    biography = forms.CharField(
        widget = forms.Textarea(
            attrs={'class': 'sssssss',
            "cols": "20", "rows": "10",},
        ),
        required=True,
        label = 'Lay bồ',
        help_text="hép",
        localize=False,
        # disabled=True,
    )

    birthday = forms.DateField(
        widget = forms.DateInput(
            attrs={"type": "date",
                'class': 'form-control'},
            format='%Y-%m-%d',
        )
    )
#     GENDER_CHOICES = [
#     (_("Male"), _("Male")),
#     (_("Female"), _("Female")),
#     (_("Other"), _("Other")),
# ]
#     gender = forms.ChoiceField(
#         widget=forms.Select(
#             attrs={'class': 'form-control'},
#         ),
#         choices=GENDER_CHOICES,
#         )

    class Meta:
        model = Profile
        fields = ('avatar', 'birthday', 'gender', 'address', 'biography', 'website_url', 'facebook_url', 'instagram_url', 'twitter_url')
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        url = {'avatar', 'address', 'gender', 'website_url', 'facebook_url', 'instagram_url', 'twitter_url'}
        for i in url:
            self.fields[i].widget.attrs['class'] = 'form-control'
        self.fields['twitter_url'].required = True