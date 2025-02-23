from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q 

# Models 
from .models import Product, Category

# Create your views here.
class ProductDetail(generic.DetailView):
    model = Product 
    template_name = 'product_shop/product_detail.html'
    context_object_name = 'product_detail'
    pk_url_kwarg = 'pk'


def search_product(request):
    # Get the query 
    query = request.GET.get('q', '').strip() 
    category_id = request.GET.get('category', '').strip()
    categories = Category.objects.all()   
    results = Product.objects.all()

    # Template 
    template = 'product_shop/search_product.html'
    
    # Debugging: print di terminal Django
    print("Query:", query)
    # print("Category:", categories)
    print("Category ID:", repr(category_id))

    # Check the query 
    if query:
        results = results.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) 
                )

    # Check category 
    if category_id: 
        results = results.filter(category__id=category_id)

    context = { 
        'results': results,
        'query': query,
        'categories': categories,
        'category_id': category_id,
        }

    return render(request, template, context)
