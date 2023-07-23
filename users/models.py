from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPost(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_set')
    full_name = models.CharField(max_length=300, blank=True)
    alamat = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id}. {self.username}  {self.full_name}" # type: ignore