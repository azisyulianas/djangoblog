from django import forms

from .models import BlogPostModel, CategoryModel

class PostBlogForms(forms.Form):
    
    class Meta:
        model = BlogPostModel
        fields = (
            'title',
            'author',
            'category',
            'text',
        )

class PostCategoryForms(forms.Form):

    class Meta:
        fields = (
            'name'
        )   