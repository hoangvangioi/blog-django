from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account, Profile
from django.utils.translation import gettext_lazy as _


# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    search_fields = ('email', 'first_name', 'last_name')

    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    # )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    # filter_horizontal = (
    #     "groups",
    #     "user_permissions",
    # )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug',)
    list_display_links = ()
    readonly_fields = ()
    ordering = ()
    search_fields = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)