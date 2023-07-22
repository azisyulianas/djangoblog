from django.shortcuts import redirect, render
from django.views import generic
from .models import BlogPostModel, CategoryModel
from django.utils.text import slugify

# Create your views here.

# Blog Views for Blogs
class HomeViews(generic.View):
    modelBlog = BlogPostModel
    modelCategory = CategoryModel
    template_name = "blogs/index.html"
    konten = {
        'judul':f'Posts All',
        'posts':modelBlog.objects.order_by('createAt').all(),
        'categories':modelCategory.objects.order_by('name').all()
    }
    
    def get(self, request, **kwargs):
        if 'category' in kwargs:
            category = self.modelCategory.objects.get(slug=kwargs['category'])
            posts = self.modelBlog.objects.filter(category=category.id) # type: ignore
            self.konten['posts']=posts
            self.konten['judul']=f'Posts by category {kwargs["category"]}'

        else:
            self.konten['posts']=self.modelBlog.objects.order_by('createAt').all()
            self.konten['judul']='Posts All'

        return render(request, self.template_name, context=self.konten)

class SingelPostViews(generic.View):
    template_name = "blogs/singlepost.html"
    modelBlog = BlogPostModel
    konten = {}

    
    def get(self, request, **kwargs):
        post = self.modelBlog.objects.get(slug=kwargs['slug'])
        self.konten['post']=post

        return render(request, self.template_name, context=self.konten)
    
class CreateViews(generic.View):
    modelBlog = BlogPostModel
    modelCategory = CategoryModel
    template_name = "blogs/create.html"
    konten = {
        'judul':'Create Post',
        'categories':modelCategory.objects.order_by('name').all()
    }
    
    # View Create
    def get(self, request, **kwargs):
        if 'slug' in kwargs:
            post = self.modelBlog.objects.get(slug=kwargs['slug'])
            self.konten['post']= post
            self.konten['judul']= f"Edit {post.title}"
        else:
            self.konten = {
                'judul':'Create Post',
                'categories':self.modelCategory.objects.order_by('name').all()
            }


        return render(request, self.template_name, context=self.konten)
    
    def post(self, request, *args, **kwargs):
        category = self.modelCategory.objects.get(slug=request.POST.get('category'))
        print(kwargs)
        # Update Post
        if 'slug' in kwargs:
            update = self.modelBlog.objects.get(slug=kwargs['slug'])
            update.title = request.POST.get('title')
            update.category = category
            update.text = request.POST.get('text')
            update.save()

            return redirect("blog:detail", slug=slugify(request.POST.get('title')))
        
        # Create Post
        created = self.modelBlog(
            title=request.POST.get('title'),
            author=request.user,
            category=category, # type: ignore
            text=request.POST.get('text'),
        )
        created.save()
        
        return redirect("blog:detail", slug=slugify(request.POST.get('title')))

def delete(request, slug):
    post = BlogPostModel.objects.get(slug=slug)
    post.delete()
    return redirect("blog:index")

# Blog Views for Category