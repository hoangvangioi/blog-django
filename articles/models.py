from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from datetime import date, datetime

from taggit.managers import TaggableManager
from .utils import unique_slug_generator, count_words, read_time
from base.fields import WEBPField
from category.models import Category
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Article(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	category 		= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
	title 			= models.CharField(max_length=255)
	slug 			= models.SlugField(max_length=250, unique_for_date='date_published')
	author 			= models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles')
	body 			= RichTextUploadingField()
	previous_post 	= models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
	next_post 		= models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
	date_published 	= models.DateTimeField(default=timezone.now)
	date_created 	= models.DateTimeField(auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True)
	status 			= models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	featured_image	= WEBPField(upload_to='images/%Y/%m/%d/', blank=True, null=True)
	image_credit 	= models.CharField(max_length=250, null=True, blank=True)
	tags 			= TaggableManager(blank=True)
	views			= models.PositiveIntegerField(default=0)
	count_words 	= models.CharField(max_length=50, default=0)
	read_time 		= models.CharField(max_length=50, default=0)
	keywords 		= models.CharField(help_text='keywords SEO (eg: python, java, html, css, assembly ...)', max_length=50, blank=True)
	description 	= models.CharField(max_length=100, blank=True)

	class Meta:
		ordering = ('-date_published',)
		verbose_name = ("Article")
		verbose_name_plural = ("Articles")

	def __str__(self):
		return self.title

	def featured_image_url (self):
		if self.featured_image: 
			return self.featured_image.url
		return static("images/no-picture-available.webp")		

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title, allow_unicode=False)
		self.count_words = count_words(self.body)
		self.read_time = read_time(self.body)
		super(Article, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('article_detail', kwargs={'slug': self.slug})


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver, sender=Article)


@receiver(post_delete, sender=Article)
def submission_delete(sender, instance, **kwargs):
	"""Deletes the image of a blog-post when the correlating BlogPost is deleted"""
	instance.featured_image.delete(False)


def check_comments_input_allowed(obj):
	"""
	Return False if obj's publish is older than 2 years.
	"""
	obj_date = obj.date_published.date()
	obj_time = obj.date_published.time()
	in2years_date = date(obj_date.year + 2, obj_date.month, obj_date.day)
	in2years = timezone.make_aware(datetime.combine(in2years_date, obj_time))
	if timezone.now() > in2years:
		return False
	else:
		return True