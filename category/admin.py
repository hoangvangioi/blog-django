from django.contrib import admin
from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'image', 'date_created')
    list_filter = ('name', )
    search_fields = ('name',)
    ordering = ['name', ]


admin.site.register(Category, CategoryAdmin)