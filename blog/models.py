from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id}.  {self.name}" # type: ignore

class BlogPostModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='author_article_set')
    category = models.ForeignKey(CategoryModel, null=True, on_delete=models.CASCADE)
    text = models.TextField()
    slug = models.SlugField(editable = False, blank = True, unique=True)
    createAt    = models.DateTimeField(auto_now_add = True)
    updateAt    = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}.  {self.title}" # type: ignore