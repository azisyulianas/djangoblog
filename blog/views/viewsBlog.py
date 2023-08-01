from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views import generic

from users.models import UserPost
from blog.models import BlogPostModel, CategoryModel, CommentModel


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
        category=None
        search=None
        if request.GET.get('page') != None:
            page = request.GET.get('page')

        if request.GET.get('key') != None:
            search = request.GET.get('key')  

        posts = BlogPostModel.objects.cari(category=category, key=search)

        if 'category' in kwargs:
            category = kwargs["category"]
            posts = BlogPostModel.objects.cari(category=category, key=search)
            posts_pagi = Paginator(posts, paginator)

            if posts_pagi.num_pages >= int(page) and int(page)>0:
                self.konten['judul']=f'Posts by category {category}'
                self.konten['posts']= posts_pagi.page(page)

                return render(request, self.template_name, context=self.konten)
            else:
                return HttpResponse(f'Total Page Count is Less Than Page or Page is Less Than Zero')

        posts_pagi = Paginator(posts, paginator)

        if posts_pagi.num_pages >= int(page) and int(page)>0:
            self.konten['posts']= posts_pagi.page(page)
            self.konten['judul']='Posts All'
        
            return render(request, self.template_name, context=self.konten)
        else:
            return HttpResponse(f'Total Page Count is Less Than Page or Page is Less Than Zero')

        

class SingelPostViews(generic.View):
    template_name = "blogs/singlepost.html"
    modelBlog = BlogPostModel
    

    def get(self, request, **kwargs):
        post = BlogPostModel.objects.get(slug=kwargs['slug'])
        comentaries = CommentModel.objects.filter(post=post).order_by('-createAt')
        
        userpost = ""
        if request.user.is_authenticated:
            userpost = UserPost.objects.get(username=request.user)

        if 'delete' in  request.GET:
            comment = CommentModel.objects.get(id=request.GET.get('delete'))
            comment.delete()

            return redirect("blog:detail", slug=kwargs['slug'])
        
        konten = {
            'post':post,
            'comentaries':comentaries,
            'userpost':userpost
        }

        return render(request, self.template_name, context=konten)
        # return dd(konten)
        
    def post(self, request, **kwargs):
        post = BlogPostModel.objects.get(slug=kwargs['slug'])
        userpost = UserPost.objects.get(username=request.user)
        if 'edit' in request.GET:
            comment = CommentModel.objects.get(id=request.GET.get('edit'))
            comment.comment = request.POST.get('comment')
            comment.post = post
            comment.save()

            return redirect("blog:detail", slug=kwargs['slug'])

        comment = CommentModel(
            comment=request.POST.get('comment'),
            post=post,
            user=userpost
        )
        comment.save()

        return redirect("blog:detail", slug=kwargs['slug'])


    
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
        
       

def deletepost(request, slug):
    post = BlogPostModel.objects.get(slug=slug)
    if post.author == request.user or request.user.is_superuser or request.user.groups.filter(name='admin').exists():
        post.delete()
        return redirect("blog:index")
    else:
        raise PermissionDenied()
