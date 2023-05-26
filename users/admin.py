from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib import messages
from django.utils.translation import ngettext

from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    show_change_link = True
    extra = 3
    can_delete = False
    readonly_fields = ['updated_on']
    fieldsets = (
        (None,
            {
                "fields": (("avatar", "address"), ("job_title", "bio"))
            },
        ),
        ('Social Network',
            {
                "fields": (( 'twitter_url', 'instagram_url'), ('facebook_url', 'github_url'))
            }
        ),
        ('Date information',
            {
                "fields": (( 'created_on', 'updated_on'), ),
                'classes': ('collapse', 'collapse-closed'),
            }
        )
    )


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    # add_form_template = "admin/users/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None,
            {
                "fields": (
                    (("name", "email", ), "password", "is_active", )
                )
            },
        ),
        ("Date Information",
            {
                "fields": (("date_joined", "last_login"),),
                "classes": ("collapse"),
            },
        ),
        ('Permissions', 
            {
                'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
                'classes': ('collapse', 'collapse-closed'),
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("email", "name", "last_login", "is_active", "date_joined")
    list_display_links = ("email",)
    ordering = ("id",)
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    search_fields = ("name", "email")
    date_hierarchy = "date_joined"
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    inlines = [ProfileInline]
    actions = ['activate_user','deactivate_user']

    def activate_user(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, ngettext(
            '%d user was successfully marked as Activate.',
            '%d users were successfully marked as Activate.',
            updated,
        ) % updated, messages.SUCCESS)
    
    def deactivate_user(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, ngettext(
            '%d user was successfully marked as Deactivate.',
            '%d users were successfully marked as Deactivate.',
            updated,
        ) % updated, messages.SUCCESS)

    activate_user.short_description = u"Activate selected users"
    deactivate_user.short_description = u"Deactivate selected users"