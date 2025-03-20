from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
)
from django.db.models import Q 
from django.contrib.auth.decorators import login_required

# Models 
from .models import Product, Category

# Create your views here.
def product_detail(request, pk):
    product_data = Product.objects.all()
    template_name = "product_shop/product_detail.html"
    context = {"product_detail": product_data}
    return render(request, template_name, context)

class ProductDetail(DetailView):
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
        }

    return render(request, template, context)

@login_required
def add_product(request):
    # Identified the user seller or not 
    if request.user.role != "SELLER":
        return HttpResponseForbidden("Only Seller can add product")

    # Templates 
    template = "product_shop/add_product.html"

    # Add form to add the product 
    if request.method == "POST":
        # Add the form 
        form = AddProductForm(requets.POST, request.FILES)
        
        # Check the forms valid or not 
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user

    # Add context for django template
    context = {"add_product_form": form}

    # Render the result 
    return render(request, template, context)
