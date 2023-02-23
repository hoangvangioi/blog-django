from django import forms
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .models import Contact


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(max_length=120,
                        required=True,
                        label=_("Name"),
                        error_messages={'required': 'Please enter your name',},
                        widget=forms.TextInput(
                            attrs={'placeholder': "Please input your name",
                            'tabindex' : 0,
                            'arial-label' : "Please input your name"
                            }))
    email = forms.EmailField(required=True, 
                        label=_('Email Address'),
                        error_messages={'invalid': "A first name must start in upper case."},
                        widget=forms.EmailInput(
                            attrs={'placeholder': "Please input email address",
                            'tabindex' : 0, 
                            'arial-label' : "Please input email address" 
                            }))
    subject = forms.CharField(max_length=255,
                            required=True,
                            label=_('Subject'),
                            error_messages={'invalid': "A first name must start in upper case."},
                            widget=forms.TextInput(
                                attrs={'placeholder': "Please input subject",
                                    'tabindex' : 0, 
                                    'role' : "input",
                                    'arial-label' : "Please input subject"
                                }))
    message = forms.CharField(required=True,
                            label=_('Message'),
                            error_messages={'invalid': "A first name must start in upper case."},
                            widget=forms.Textarea(
                                attrs={'rows': 8,
                                        'cols': 15,
                                        'placeholder': "Write here your message!",
                                        'tabindex' : 0, 
                                        'aria-label' : "leave a message"
                            }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['class'] = 'text-base leading-none text-gray-900 p-3 focus:oultine-none focus:border-indigo-700 mt-4 bg-gray-100 border rounded border-gray-200 placeholder-gray-100'
        self.fields['email'].widget.attrs['class'] = 'text-base leading-none text-gray-900 p-3 focus:oultine-none focus:border-indigo-700 mt-4 bg-gray-100 border rounded border-gray-200 placeholder-gray-100'
        self.fields['subject'].widget.attrs['class'] = 'text-base leading-none text-gray-900 p-3 focus:oultine-none focus:border-indigo-700 mt-4 bg-gray-100 border rounded border-gray-200 placeholder-gray-100'
        self.fields['message'].widget.attrs['class'] = 'h-36 text-base leading-none text-gray-900 p-3 focus:oultine-none focus:border-indigo-700 mt-4 bg-gray-100 border rounded border-gray-200 placeholder-gray-100 resize-none'

    class Meta:
        model = Contact
        fields = '__all__'


    def send_mail_guest(self):
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        content = render_to_string('contact/send_email.txt', {
        'full_name': full_name,
        'from_email': email,
        'message': message,
        'subject': subject,
        })

        mail = EmailMessage(
            subject='Thông báo về phản hồi của bạn',
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            headers={'Reply-To': settings.EMAIL_HOST_USER}
        )
        mail.send()


    def send_mail_admin(self):
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        content = f"Bạn vừa nhận được lời nhắn từ\n{full_name}\nE-mail: {email}\nVới nội dung là: \nsubject: {subject}\nmessage: {message}\nHãy trả lời sớm nhất có thể"

        mail = EmailMessage(
            subject=subject,
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            headers={'Reply-To': email}
        )
        mail.send()