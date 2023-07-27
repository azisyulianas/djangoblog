from django.db import models
from django.contrib.auth.models import User
from users.models import UserPost
from django.utils.text import slugify
from django.db.models import Count
from django.db.models import Q

# Create your models here.

# Query Untuk Blog Models
class BlogQuery(models.QuerySet):
    def total(self):
        return self.values('category__name','category__slug')\
                .annotate(total=Count('id'))\
                .order_by('-total')
    
    def cari(self, category=None, key=None):
        if key is None or key == "":
            if category is None:
                posts = self.filter(is_publish=True)\
                    .order_by('-createAt')
                return posts
        
            look = Q(is_publish=True) & Q(category__slug = category)
            posts = self.filter(look)\
                    .order_by('-createAt')
            return posts
        

        search = Q(title__icontains=key) | Q(text__icontains=key)
        if category is None:
            posts = self.filter(is_publish=True)\
                    .filter(search)\
                    .order_by('-createAt')
            return posts
        
        look = Q(is_publish=True) & Q(category__slug = category)
        posts = self.filter(look)\
                .filter(search)\
                .order_by('-createAt')
        return posts

# Class Untuk Memanggil Query Blog Model
class BlogManager(models.Manager):
    def query_set(self):
        return BlogQuery(self.model, using=self._db)

    def total(self,):
        return self.query_set().total()
    
    def cari(self, category=None, key=None):
        return self.query_set().cari(category=category, key=key)

# Category Model
class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id}.  {self.name}" # type: ignore

# Blog Post Model
class BlogPostModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publisher', null=True, blank=True)
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

# Comment Model
class CommentModel(models.Model):
    post = models.ForeignKey(BlogPostModel, on_delete=models.CASCADE, related_name='commentblog')
    user = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='commentuser')
    comment = models.TextField()
    createAt = models.DateTimeField(auto_now_add = True)
    updateAt = models.DateTimeField(auto_now = True)
    is_edited = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        self.is_edited = self.createAt != self.updateAt # type: ignore
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"comment id {self.id} at post {self.post.title}" # type: ignore