from django.contrib import admin

# Register your models here.
from .models import CategoryModel, BlogPostModel

class ReadOnlyBlog(admin.ModelAdmin):
    readonly_fields = [
        'slug',
        'createAt',
        'updateAt',
    ]

class ReadOnlyCategory(admin.ModelAdmin):
    readonly_fields = [
        'slug',
    ]

admin.site.register(CategoryModel, ReadOnlyCategory)
admin.site.register(BlogPostModel, ReadOnlyBlog)