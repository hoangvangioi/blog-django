from django.contrib import admin
from .models import Contact

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject',)
    list_display_links = ('full_name', 'email', 'subject',)
    search_fields = ('email', 'timestamp',)