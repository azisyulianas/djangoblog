from django.contrib import admin

# Register your models here.
from .models import CategoryModel, BlogPostModel, CommentModel

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

class ReadOnlyComment(admin.ModelAdmin):
    readonly_fields = [
        'createAt',
        'updateAt',
        'is_edited',
    ]

admin.site.register(CategoryModel, ReadOnlyCategory)
admin.site.register(BlogPostModel, ReadOnlyBlog)
admin.site.register(CommentModel, ReadOnlyComment)