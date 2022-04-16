from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext as _

# from django.conf.urls.static import static
from .utils import unique_slug_generator

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name, last_name, email, username, password=None):
        user = self.create_user(
                email = self.normalize_email(email),
                username = username,
                first_name = first_name,
                last_name = last_name,
                password=password,
                is_staff=True
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def has_perms(self, perm, obj=None):
        return self.is_admin


    # def get_full_name(self):
    #     if self.full_name:
    #         return self.full_name
    #     return self.email

    # def get_short_name(self):
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True

    # @property
    # def is_staff(self):
    #     if self.is_admin:
    #         return True
    #     return self.is_staff

    # @property
    # def is_admin(self):
    #     return self.is_admin

    # @property
    # def is_active(self):
    #     return self.active

    def get_user_permissions(self, user_obj, obj=None):
        return True

    def get_all_permissions(user_obj, obj=None):
        return True


class Profile(models.Model):

    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    slug = models.SlugField(max_length=200)
    avatar = models.ImageField(blank=True, upload_to='profile/avatars/')
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.URLField()
    facebook_url = models.URLField()
    instagram_url = models.URLField()
    twitter_url = models.URLField()
    biography = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f'{self.user}'

    def get_first_name(self):
        return f'{self.first_name}'
            
    def get_last_name(self):
        return f'{self.last_name}'
    
    def get_absolute_url(self):
        return reverse("profile", args={self.slug})

    # def save(self, *args, **kwargs):
    #     self.slug= slugify(self.user)
    #     super().save(*args, **kwargs)

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, user):
        return cls.objects.filter(user__username__icontains=user).all()

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('img/avatar.png')

    # @receiver(post_save, sender=Account)
    # def update_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #     instance.profile.save()

def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_category_receiver, sender=Profile)
