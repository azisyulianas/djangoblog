from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import generic

from .models import BlogPostModel, CategoryModel

# Create your views here.


# Blog Views for Category
class CategoryIndex(generic.View):
    modelBlog = BlogPostModel
    modelCategory = CategoryModel
    template_name = "blogs/category.html"
    konten = {
        'judul':f'Summaries Category',
        'summaries':modelBlog.objects.values('category__name','category__slug')\
                .annotate(total=Count('id'))\
                .order_by('-total').all(),
        'categories':modelCategory.objects.order_by('name').all()
    }

    def get(self, request, **kwargs):
        self.konten['categories']=self.modelCategory.objects.order_by('name').all()
        return render(request, self.template_name, context=self.konten)
    
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            name = request.POST.get('name')

            # Cek if have
            if not self.modelCategory.objects.filter(name=name).exists():
                category = self.modelCategory(name=name)
                category.save()
    
                return JsonResponse({
                    'message':'Data Berhasil Ditambahkan'
                })

            return JsonResponse({
                    'message':'Data Sudah Ada'
                })
        
class CategoryEdit(generic.View):
    modelCategory = CategoryModel
    template_name = "blogs/editcategory.html"
    konten = {}

    def get(self, request, **kwargs):
        self.konten['category']=self.modelCategory.objects.get(slug=kwargs['slug'])
        return render(request, self.template_name, context=self.konten)
    
    def post(self, request, **kwargs):
            name = request.POST.get('name')
            category = self.modelCategory.objects.get(slug=kwargs['slug'])
            category.name = name
            category.save()

            return redirect("blog:indexcategory")
