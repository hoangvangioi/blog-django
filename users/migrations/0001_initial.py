# Generated by Django 4.1.7 on 2023-03-05 01:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('key', models.CharField(max_length=40)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='creation timestamp')),
                ('purpose', models.CharField(choices=[('E', 'Change E-Mail')], max_length=1)),
                ('notifications', models.SmallIntegerField(default=0, help_text='homw many times has been notified', verbose_name='notifications counter')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('avatar', models.ImageField(blank=True, upload_to='profile_pics')),
                ('job_title', models.CharField(blank=True, max_length=100)),
                ('bio', models.CharField(blank=True, help_text='Short Bio (eg. I love cats and games)', max_length=250)),
                ('address', models.CharField(blank=True, help_text='Enter Your Address', max_length=100)),
                ('twitter_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('instagram_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('facebook_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('github_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
