from django.db import models
from django.contrib.auth.models import User
from PIL import Image

import os
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "iamge_%s.%s" % (instance.username.username, ext)
    return os.path.join('image', filename)

# Create your models here.
class UserPost(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='useradd')
    full_name = models.CharField(max_length=300, blank=True, editable=True)
    alamat = models.TextField(blank=True, editable=True)
    bio = models.TextField(blank=True, editable=True)
    image = models.ImageField(upload_to=content_file_name, blank=True)

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path) # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)
        
        return super().save()

    def __str__(self):
        return f"{self.id}. {self.username}  {self.full_name}" # type: ignore