from users.forms import RegisterForms
from users.models import UserPost

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views import generic

# Create your views here.
    
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

