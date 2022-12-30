from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article


class ArticleForm(forms.ModelForm):
                                                      
    body = forms.CharField(
        required=True,
        widget=CKEditorUploadingWidget()
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