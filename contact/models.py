from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Contact(models.Model):
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=255)
    email = models.EmailField(verbose_name=_('Email'))
    subject = models.CharField(verbose_name=_('Subject'), max_length=255)
    message = models.TextField(verbose_name=_('Message'))
    timestamp = models.DateTimeField(verbose_name=_('Date created') ,auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['timestamp']
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')