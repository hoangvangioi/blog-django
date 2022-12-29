from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from category.models import Category
from .models import Article


class ArticleForm(forms.ModelForm):
                                                      
    body = forms.CharField(
        required=True,
        widget=CKEditorUploadingWidget(
            attrs={
                'class': 'w-full p-3 mt-4 border border-gray-300 rounded outline-none focus:bg-green-200'
            }
        )
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
            'body',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'w-full p-3 mt-4 border border-gray-300 rounded outline-none focus:bg-green-200'
            # self.fields['status'].widget.attrs['class'] = 'relative flex items-center justify-between w-full px-5 py-4 dropbtn-one'
            # self.fields['myfield'].widget.attrs.update({'class': 'myfieldclass'})