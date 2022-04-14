from email.policy import default
from category.models import Category
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from .utils import unique_slug_generator


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
	featured_image	= models.ImageField(upload_to='images/%Y/%m/%d/', default='Great-Tshirt.jpg')
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


class Comment(MPTTModel):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	content = RichTextField()
	publish = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=True)

	class MPTTMeta:
		order_insertion_by = ['publish']

	def __unicode__(self):
		return self.post


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)