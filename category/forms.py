from dataclasses import field
from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    
    category = forms.CharField(
        label = 'Thêm danh mục',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-6 mt-3 mb-3'}
        )
    )
    class Meta:
        model = Category
        fields = ("category",)