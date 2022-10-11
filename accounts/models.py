from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.dispatch import receiver
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError(_('User must have an email address'))

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
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

    def create_staffuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
                email = self.normalize_email(email),
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
    email           = models.EmailField(max_length=100, unique=True)
    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        
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