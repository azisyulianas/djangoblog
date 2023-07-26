from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count

# Create your models here.

class BlogQuery(models.QuerySet):
    def total(self):
        return self.values('category__name','category__slug')\
                .annotate(total=Count('id'))\
                .order_by('-total')

class BlogManager(models.Manager):
    def query_set(self):
        return BlogQuery(self.model, using=self._db)

    def total(self,):
        return self.query_set().total()

class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id}.  {self.name}" # type: ignore

class BlogPostModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_article_set')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publisher_article_set', null=True, blank=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    is_publish = models.BooleanField(default=False, blank=True)
    createAt    = models.DateTimeField(auto_now_add = True)
    updateAt    = models.DateTimeField(auto_now = True)

    objects=BlogManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}.  {self.title}" # type: ignore