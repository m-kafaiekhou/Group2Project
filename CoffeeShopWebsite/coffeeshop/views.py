from django.shortcuts import render
from django.views import View
from menus.models import CafeItem
from django.views.generic import ListView,TemplateView
# Create your views here.


class HomePage(View):
    template_name = "coffeeshop/home.html"

    def get(self, request, *args, **kwargs):
        # top_rated_items = CafeItem.top_rated_items()
        return render(request, self.template_name, {"top_rated_items": None})

'''class HomePage(TemplateView):
    template_name = "coffeeshop/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_rated_items'] = None
        return context'''


class GalleryPage(View):
    template_name = "coffeeshop/gallery.html"

    def get(self, request, *args, **kwargs):
        items = CafeItem.objects.all()
        context = {"items":items}
        return render(request, self.template_name, context)

'''class GalleryPage(ListView):
    template_name = "coffeeshop/gallery.html"
    model = CafeItem
    context_object_name = "items "
'''