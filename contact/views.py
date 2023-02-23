from django.urls import reverse
from django.contrib import messages
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from .forms import ContactForm

# Create your views here.


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm

    def form_valid(self, form):
        try:
            form.save()
            form.send_mail_guest()
            form.send_mail_admin()
            messages.success(self.request, _('Thank you for your message. It has been sent.'))
        except:
            messages.error(self.request, _('One or more fields have an error. Please check and try again.'))
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('contact')