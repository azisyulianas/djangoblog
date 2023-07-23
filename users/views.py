from django.shortcuts import redirect, render
from django.views import generic
from blog.models import BlogPostModel
from .models import UserPost
from .forms import RegisterForms
from django.contrib.auth.models import Group

# Create your views here.
class IndexUsers(generic.View):
    template_name = "users/index.html"
    modelBlog = BlogPostModel
    modelUser = UserPost
    konten = {}
    

    def get(self, request, **kwargs):
        posts = self.modelBlog.objects.filter(author__username=kwargs['user'])
        users = self.modelUser.objects.get(username__username=kwargs['user'])
        self.konten['posts']=posts
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
    
class RegisterViews(generic.View):
    template_name = "users/register.html"
    modelUser = UserPost
    modelGroup = Group
    konten = {}


    def get(self, request, **kwargs):
        self.konten['forms']=RegisterForms()
        return render(request, self.template_name, self.konten)
    
    def post(self, request, *args, **kwargs):
        form = RegisterForms(request.POST)
        self.konten['forms']=form
        group = self.modelGroup.objects.get(name="author")
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            user.groups.add(group)
            user_detailed = self.modelUser(username=user)
            user_detailed.save()
            return redirect('user:list')
        else:
            return render(request, self.template_name, self.konten)
    
