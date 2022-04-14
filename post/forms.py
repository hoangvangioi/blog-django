from ckeditor.widgets import CKEditorWidget
from django import forms
from mptt.forms import TreeNodeChoiceField
from tinymce.widgets import TinyMCE

from .models import Comment, Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                    'placeholder': 'Nhập tiêu đề bài viết'
            }
        )
    )
    body = forms.CharField(
        widget= CKEditorWidget(
            
        )
    )

    featured_image = forms.ImageField(required=True, 
        widget=forms.FileInput(attrs={
            'class': 'form-control'
            }))

    class Meta:
        model = Post
        fields = ('title', 
                'body', 
                'previous_post', 
                'next_post', 
                'status',
                'featured_image',
                'category',
                'tags',
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'cols': 3, 'rows': 3}
            )
            )
    # content = forms.CharField(widget = CKEditorWidget())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
            )
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('parent', 'content')

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(CommentForm, self).save(*args, **kwargs)