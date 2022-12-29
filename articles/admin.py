from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Article


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    """
    Admin for Article model.
    """
    list_display = ('title', 'slug', 'author', 'image_credit', 'date_published', 'status')
    list_display_links = ('title', 'slug')
    list_filter = ('status', 'date_created', 'date_published', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_published'
    ordering = ('status', '-date_created')
    readonly_fields = ('views', 'count_words', 'read_time')

    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status', 'author',), 'body',)}),
        (_('Illustration'), {
            'fields': ('featured_image', 'image_credit'),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Publication'), {
            'fields': ('date_published', ),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Slug'), {
            'fields': ('slug', ),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Post other'), {
            'fields': ('previous_post', 'next_post',),
            'classes': ('collapse', 'collapse-closed')}),
        (_('SEO'), {
            'fields': ('keywords', 'description',),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Metadatas'), {
            'fields': ('views', 'count_words', 'read_time',),
            'classes': ('collapse', 'collapse-closed')}),
        (None, {'fields': (('category', 'tags', ), )}))

    sortable_by = ('date_published', )
    actions_on_top = True
    actions_on_bottom = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(ArticleAdmin, self).__init__(model, admin_site)


# Registers the article model at the admin backend.
admin.site.register(Article, ArticleAdmin)