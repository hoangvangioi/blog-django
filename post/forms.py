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
        # widget= CKEditorWidget(
            
        # )


        widget=CKEditorWidget(
            attrs={
                'class': 'form-control'
            }
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



















        #         'config'={
        #     'toolbar': [
        #         {
        #             'name': 'document',
        #             'groups': [ 'mode', 'document', 'doctools' ],
        #             'items': [ 'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates' ]
        #         },
        #         {
        #             'name': 'clipboard',
        #             'groups': [ 'clipboard', 'undo' ],
        #             'items': [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ]
        #         },
        #         {
        #             'name': 'editing',
        #             'groups': [ 'find', 'selection', 'spellchecker' ],
        #             'items': [ 'Find', 'Replace', '-', 'SelectAll' ]
        #         },
        #         {
        #             'name': 'forms',
        #             'items': [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ]
        #         },
        #         '/', # Linebreak
        #         {
        #             'name': 'basicstyles',
        #             'groups': [ 'basicstyles', 'cleanup' ],
        #             'items': [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ]
        #         },
        #         {
        #             'name': 'paragraph',
        #             'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ],
        #             'items': [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl' ]
        #         },
        #         {
        #             'name': 'links',
        #             'items': [ 'Link', 'Unlink', 'Anchor' ]
        #         },
        #         {
        #             'name': 'insert',
        #             'items': [ 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe' ]
        #         },
        #         '/', # Linebreak
        #         {
        #             'name': 'styles',
        #             'items': [ 'Styles', 'Format', 'Font', 'FontSize' ]
        #         },
        #         {
        #             'name': 'colors',
        #             'items': [ 'TextColor', 'BGColor' ]
        #         },
        #         {
        #             'name': 'tools',
        #             'items': [ 'Maximize', 'ShowBlocks' ]
        #         },
        #         {
        #             'name': 'others',
        #             'items': [ '-' ]
        #         },
        #         {
        #             'name': 'about',
        #             'items': [ 'About' ]
        #         }
        #     ],
        #     'height': 291,
        #     'width': '100%',
        #     'toolbarGroups': [
        #             {'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ]},
        #             {'name': 'clipboard', 'groups': [ 'clipboard', 'undo' ]},
        #             {'name': 'editing', 'groups': [ 'find', 'selection', 'spellchecker' ]},
        #             {'name': 'forms'},
        #             '/',
        #             {'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ]},
        #             {'name': 'paragraph', 'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ]},
        #             {'name': 'links'},
        #             {'name': 'insert'},
        #             '/',
        #             {'name': 'styles'},
        #             {'name': 'colors'},
        #             {'name': 'tools'},
        #             {'name': 'others'},
        #             {'name': 'about'}
        #     ]
        # }