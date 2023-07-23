from django.shortcuts import redirect, render
from django.views import generic
from blog.models import BlogPostModel
from .models import UserPost
from .forms import RegisterForms
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

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
        if request.user.is_superuser or request.user.groups.filter(name='admin').exists():
            self.konten['forms']=RegisterForms()
            return render(request, self.template_name, self.konten)
        else:
            raise PermissionDenied()
    
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
            return redirect('users:list')
        else:
            return render(request, self.template_name, self.konten)
    
class UserEditViews(generic.View):
    template_name = "users/edit.html"
    modelUser = UserPost
    konten = {}

    def get(self, request, *args, **kwargs):
        if kwargs['user'] == request.user or request.user.is_superuser or request.user.groups.filter(name='admin').exists():
            self.konten['user']=self.modelUser.objects.get(username__username=kwargs['user'])
            return render(request, self.template_name, self.konten)
        else:
            raise PermissionDenied()
    
    def post(self, request, *args, **kwargs):
        
        user = self.modelUser.objects.get(username__username=kwargs['user'])
        name = request.POST.get('name')
        alamat = request.POST.get('alamat')
        user.full_name = name
        user.alamat = alamat
        user.save()
        return redirect('users:index', user=kwargs['user'])
    
class LoginViews(generic.View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect('users:index', user=username)
        else:
            messages.error(request,"Invalid username or password.")

@login_required
def Logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("blog:index")

