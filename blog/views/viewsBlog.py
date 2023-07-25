from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views import generic

from blog.models import BlogPostModel, CategoryModel


# Blog Views for Blogs
class HomeViews(generic.View):
    modelBlog = BlogPostModel
    modelCategory = CategoryModel
    template_name = "blogs/index.html"
    konten = {
        'judul':f'Posts All',
        'posts':modelBlog.objects.filter(is_publish=True).order_by('-createAt'),
        'categories':modelCategory.objects.order_by('name')
    }
    
    def get(self, request, **kwargs):
        page = 1
        paginator = 10

        if request.GET.get('page') != None:
            page = request.GET.get('page')

        posts = self.modelBlog.objects.filter(is_publish=True).order_by('-createAt')

        if 'category' in kwargs:
            posts = self.modelBlog\
                    .objects\
                    .filter(category__slug=kwargs['category'], is_publish=True)\
                    .order_by('-createAt')
            posts_pagi = Paginator(posts, paginator)

            if posts_pagi.num_pages >= int(page) and int(page)>0:
                self.konten['judul']=f'Posts by category {kwargs["category"]}'
                self.konten['posts']= posts_pagi.page(page)

                return render(request, self.template_name, context=self.konten)
            else:
                return HttpResponse(f'Total Page Count Is Less Than Page or Less Than Zero')

        posts_pagi = Paginator(posts, paginator)

        if posts_pagi.num_pages >= int(page) and int(page)>0:
            self.konten['posts']= posts_pagi.page(page)
            self.konten['judul']='Posts All'
        
            return render(request, self.template_name, context=self.konten)
        else:
            return HttpResponse(f'Total Page Count Is Less Than Page or Less Than Zero')

        

class SingelPostViews(generic.View):
    template_name = "blogs/singlepost.html"
    modelBlog = BlogPostModel
    konten = {}

    def get(self, request, **kwargs):
        post = self.modelBlog.objects.get(slug=kwargs['slug'])
        self.konten['post']=post

        return render(request, self.template_name, context=self.konten)
    
class CreateViews(LoginRequiredMixin, generic.View):
    login_url = "/"
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
            if post.author == request.user or request.user.is_superuser or request.user.groups.filter(name='admin').exists():
                self.konten['post']= post
                self.konten['judul']= f"Edit {post.title}"
                return render(request, self.template_name, context=self.konten)
            else:
                raise PermissionDenied()
        else:
            self.konten = {
                'judul':'Create Post',
                'categories':self.modelCategory.objects.order_by('name').all()
            }
            return render(request, self.template_name, context=self.konten)
        
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        checked = False
        if 'publish' in request.POST:
            checked = True
            publisher = request.user
        
        if self.modelCategory.objects.filter(slug=request.POST.get('category')).exists():

            category = self.modelCategory.objects.get(slug=request.POST.get('category'))
            print(kwargs)
            
            # Update Post
            if 'slug' in kwargs:
                post = self.modelBlog.objects.get(slug=kwargs['slug'])
                if post.author == request.user or request.user.is_superuser or request.user.groups.filter(name='admin').exists():
                    post.title = request.POST.get('title')
                    post.category = category
                    post.text = request.POST.get('text')
                    if request.user.groups.filter(name='admin').exists():
                        post.is_publish = checked
                        post.publisher = publisher # type: ignore

                    post.save()
                    return redirect("blog:detail", slug=slugify(request.POST.get('title')))
                else:
                    raise PermissionDenied()
                
            # Create Post
            post = self.modelBlog(
                title=request.POST.get('title'),
                author=request.user,
                category=category, # type: ignore
                text=request.POST.get('text'),
            )
            if checked:
                post.publisher = publisher # type: ignore
                post.is_publish = checked

            post.save()
            
            return redirect("blog:detail", slug=slugify(request.POST.get('title')))  
        else:
            return render(request, self.template_name, context=self.konten) 
        
       

def delete(request, slug):
    post = BlogPostModel.objects.get(slug=slug)
    if post.author == request.user or request.user.is_superuser or request.user.groups.filter(name='admin').exists():
        post.delete()
        return redirect("blog:index")
    else:
        raise PermissionDenied()