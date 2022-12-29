from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    
    name = forms.CharField(
        label = 'Thêm danh mục',
        widget=forms.TextInput(
            attrs={'class': 'border border-gray-300 dark:border-gray-700 pl-3 py-3 shadow-sm rounded text-sm focus:outline-none focus:border-indigo-700 bg-transparent placeholder-gray-500 text-gray-600 dark:text-gray-400'}
        )
    )
    class Meta:
        model = Category
        fields = ("name",)