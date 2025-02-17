from django.shortcuts import render
from django.views import generic
from product_shop.models import Product


# Create your views here.
class Home(generic.TemplateView):
    template_name = "base/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_list"] = Product.objects.all()
        return context
