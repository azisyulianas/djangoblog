from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import generic

from blog.models import BlogPostModel, CategoryModel

# Create your views here.


# Blog Views for Category
class CategoryIndex(generic.View):
    modelBlog = BlogPostModel
    modelCategory = CategoryModel
    template_name = "blogs/category.html"
    konten = {
        'judul':f'Summaries Category',
        'categories':modelCategory.objects.order_by('name').all()
    }

    def get(self, request, **kwargs):
        query = BlogPostModel.objects.total()[:10]
        self.konten['categories']=self.modelCategory.objects.order_by('name').all()
        self.konten['summaries']=query
        total = [i['total'] for i in query]
        label = [i['category__name'] for i in query]
        self.konten['total']=total
        self.konten['label']=label
        # return dd(self.konten)
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
                    'message':'Data Berhasil Ditambahkan',
                    'status':True
                })

            return JsonResponse({
                    'message':'Data Sudah Ada',
                    'status':False
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
