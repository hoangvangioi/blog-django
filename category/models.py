from django.db import models
from django.urls import reverse

from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.templatetags.static import static
from base.fields import WEBPField
from .utils import unique_slug_generator

# Create your models here.


class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(max_length=100, unique=True)
    image       = WEBPField(blank=True, upload_to='category_images')
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
            return reverse('category_articles', args=[self.slug])

    def image_url (self):
        if self.image: 
            return self.image.url
        return static("images/no-picture-available.webp")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=False)
        super(Category, self).save(*args, **kwargs)

        
def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_category_receiver, sender=Category)


@receiver(post_delete, sender=Category)
def submission_delete(sender, instance, **kwargs):
    """Deletes the image of a blog-post when the correlating Category is deleted"""
    instance.image.delete(False)