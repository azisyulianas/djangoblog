from django.contrib import admin
from .models import UserPost

# Register your models here.
class ReadOnlyUser(admin.ModelAdmin):
    readonly_fields = [
        'alamat',
    ]

admin.site.register(UserPost)
