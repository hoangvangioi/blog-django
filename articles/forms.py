from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article
from category.models import Category
from django.utils.translation import  gettext_lazy as _
from django.utils.html import format_html


help_text_title = _('Please enter a short title for this article')
help_text_category = _("Please select a category for this article")
help_text_tags = _("A comma-separated list of tags.")
help_text_status = _("Please select an article status")
help_text_keywords = _("Please enter keywords for this article")
help_text_description = _("Please enter a short description for this article")
help_text_featured_image = _(u"Please upload an image that is to be used as a featured image for this article.")
help_text_image_credit = _(u"Please enter the name of the image credit if applicable.")


class ArticleForm(forms.ModelForm):

    title = forms.CharField(
        label="Article title",
        max_length=100,
        required=True,
        help_text=format_html('<p class="mt-3 text-xs leading-3 text-gray-600">{}</p>', help_text_title),
    )

    category = forms.ModelChoiceField(
        label="Category",
        queryset=Category.objects.all(),
        empty_label="(Select category)",
        help_text=format_html('<p class="mt-3 text-xs leading-3 text-gray-600">{}</p>', help_text_category),
    )

    status = forms.ChoiceField(
        label="Status",
        choices = Article.STATUS_CHOICES,
        initial = Article.STATUS_CHOICES[0][0],
        help_text=format_html('<p class="mt-3 text-xs leading-3 text-gray-600">{}</p>', help_text_status),
        required=True
    )

    keywords = forms.CharField(
        label="Keywords",
        max_length=250,
        help_text=format_html('<p class="mt-3 text-xs leading-3 text-gray-600">{}</p>', help_text_keywords),
        required=False,
    )

    description = forms.CharField(
        label="Description",
        max_length=250,
        help_text=format_html('<p class="mt-3 text-xs leading-3 text-gray-600">{}</p>', help_text_description),
        required=False,
    )

    body = forms.CharField(
        required=True,
        widget=CKEditorUploadingWidget(),
        label=_('Article content')
    )

    featured_image = forms.ImageField(
        required=False,
        label=_(u"Featured image"),
        help_text=format_html('<p class="mt-3 text-xs leading-3 text-gray-600">{}</p>', help_text_featured_image),
        error_messages={} 
    )

    image_credit = forms.CharField(
        max_length=250, 
        required=False,
        label=_(u"Image credit"),
        help_text=format_html('<p class="mt-3 text-xs leading-3 text-gray-600">{}</p>', help_text_image_credit),
    )

    previous_post = forms.ModelChoiceField(
        required=False,
        queryset=Article.objects.all(),
        label=_(u"Previous article"),
    )

    next_post =  forms.ModelChoiceField(
        required=False,
        queryset=Article.objects.all(),
        label=_(u"Next article"),
    )
    
    class Meta:
        model = Article
        fields = (
            'title',
            'category',
            'status', 
            'featured_image', 
            'image_credit', 
            'tags', 
            'keywords', 
            'description',
            'previous_post',
            'next_post',
            'body',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'w-full p-3 mt-4 border border-gray-300 rounded outline-none focus:bg-green-200'

    def add_control_label(f):
        label_attrs = 'text-base font-medium leading-none text-gray-800'
        def control_label_tag(self, contents=None, attrs=None, label_suffix=None):
            if attrs is None: attrs = {}
            attrs['class'] = label_attrs

            return f(self, contents, attrs, label_suffix) 
        return control_label_tag

    forms.BoundField.label_tag = add_control_label(forms.BoundField.label_tag)