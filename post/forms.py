from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={'invalid': "Phone number have 4-25 digits and may start with '+'."},
        widget=forms.TextInput(
            attrs={'class': 'bordder-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none',
                    'placeholder': 'Nhập tiêu đề bài viết'
            }
        )
    )
    body = forms.CharField(
        # widget= CKEditorWidget(

        # )
        required=False,


        widget=CKEditorUploadingWidget(
            attrs={
                'class': 'bordder-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )
    # previous_post = forms.ModelChoiceField(
    #         queryset=Post.published.all(),
    #         label='Bài trước')

    # next_post = forms.ModelChoiceField(
    #         queryset=Post.published.all(),
    #         label='Bài sau')

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
                'featured_image',
                'category',
                'status',
                'tags',
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'bordder-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none'