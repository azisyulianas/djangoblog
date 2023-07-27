from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views import generic
from django.core.paginator import Paginator
import os

from blog.models import BlogPostModel

from users.models import UserPost


# UserModel
class IndexUsers(generic.View):
    template_name = "users/index.html"
    modelBlog = BlogPostModel
    modelUser = UserPost
    konten = {}
    

    def get(self, request, **kwargs):
        page = 1
        paginator = 5

        if request.GET.get('page') != None:
            page = request.GET.get('page')

        posts = self.modelBlog.objects.filter(author__username=kwargs['user'])
        users = self.modelUser.objects.get(username__username=kwargs['user'])
        posts_pagi = Paginator(posts, paginator)
        self.konten['posts']=posts_pagi.page(page)
        self.konten['users']=users
        return render(request, self.template_name, self.konten)
    
class ListUser(generic.View):
    template_name = "users/list.html"
    modelUser = UserPost
    konten = {}

    def get(self, request, **kwargs):
        users = self.modelUser.objects.all()
        self.konten['users']=users
        return render(request, self.template_name, self.konten)
    
class UserEditViews(generic.View):
    template_name = "users/edit.html"
    modelUser = UserPost
    konten = {}

    def get(self, request, *args, **kwargs):
        if kwargs['user'] == request.user.username:
            self.konten['user']=self.modelUser.objects.get(username__username=kwargs['user'])
            return render(request, self.template_name, self.konten)
        else:
            raise PermissionDenied()
    
    def post(self, request, *args, **kwargs):
        
        user = self.modelUser.objects.get(username__username=kwargs['user'])
        name = request.POST.get('name')
        alamat = request.POST.get('alamat')
        bio = request.POST.get('bio')
        user.full_name = name
        user.alamat = alamat
        user.bio = bio

        if 'image' in request.FILES:
            image_path = user.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
            user.image = request.FILES.get('image')
            
        user.save()

        return redirect('users:index', user=kwargs['user'])