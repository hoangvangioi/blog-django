from category.models import Category
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from .utils import unique_slug_generator
from base.fields import WEBPField
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime


# Create your models here.


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	title 			= models.CharField(max_length=255)
	slug 			= models.SlugField(max_length=250, unique_for_date='publish')
	author 			= models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blog_posts')
	body 			= RichTextUploadingField()
	previous_post 	= models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
	next_post 		= models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
	publish 		= models.DateTimeField(default=timezone.now)
	created 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)
	status 			= models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	featured_image	= WEBPField(upload_to='images/%Y/%m/%d/', blank=True, null=True)
	category		= models.ManyToManyField(Category)
	tags 			= TaggableManager()
	objects = models.Manager()  # The default manager.
	published = PublishedManager()  # Our custom manager.

	class Meta:
		ordering = ('-publish',)
		verbose_name = ("post")
		verbose_name_plural = ("posts")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail',
					   args=[self.publish.year,
							self.publish.month,
							self.publish.day,
							self.slug])







def check_comments_input_allowed(obj):
    """
    Return False if obj's publish is older than 2 years.
    """
    obj_date = obj.publish.date()
    obj_time = obj.publish.time()
    in2years_date = date(obj_date.year + 2, obj_date.month, obj_date.day)
    in2years = timezone.make_aware(datetime.combine(in2years_date, obj_time))
    if timezone.now() > in2years:
        return False
    else:
        return True