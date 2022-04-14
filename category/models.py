from django.db import models
from django.urls import reverse
from .utils import unique_slug_generator
from django.db.models.signals import pre_save


# Create your models here.


class Category(models.Model):
    category    = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
            return reverse('post_by_category', args=[self.slug])

    def __str__(self):
        return self.category


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_category_receiver, sender=Category)