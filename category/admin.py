from django.contrib import admin

from post.models import Post
from .models import Category

# Register your models here.

# class PostInline(admin.StackedInline):
#     model = Post

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category',)}
    list_display = ('category', 'slug')
    # inlines = [PostInline]
admin.site.register(Category, CategoryAdmin)