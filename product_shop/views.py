"""
Product Shop Module

This module handle everything about product view in web.
* Function:
------------------
 ** product_detail()
    Show the detail about product filter by ID

 ** search_product(q: str)
    Search product based on q(query) that user given

 ** add_product(user: User, product_data: dict)
    Add new product into shop, only can be used by SELLER

* Note:
------------------
 ** Only user with SELLER role can add new product
 ** The search function using name, category, and description for filtering
"""

# Django Library
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.http import HttpResponseForbidden
# from django.urls import reverse_lazy
# from django.views.generic import (
#     DetailView,
# )
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import model_to_dict

# Forms
from .forms import (
    AddProductForm,
    CategoryForm,
)

# Models
from .models import (
    Product,
    ProductImage,
    Category,
)
from orders_shop.models import (
    OrderItem,
    OrderDetail,
)

# Create your views here.
def product_detail(request, pk):
    """
    Retrieve and return the detail product based on its ID

    Parameters:
        request (HttpRequest): The HTTP request object
        pk (str): The product ID to retrieve

    Returns:
        HttpResponse: Rendered HTML with product detail
    """
    product = get_object_or_404(Product, pk=pk)
    data = model_to_dict(product)
    order_items = OrderItem.objects.filter(user_id=request.user, order_status="pending")
    order_detail = OrderDetail.objects.filter(
        order_id__in = order_items,
        product_id=product,
    ).first()
    template_name = "product_shop/product_detail.html"
    context = {
        "product_detail": product,
        "data_dict": data,
        "order_detail": order_detail,
        }
    return render(request, template_name, context)

# Search View
def search_product(request):
    """
    Search and return the data after filtering by query

    Parameters:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Rendered HTML with filtering data
    """
    # Get the query
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    categories = Category.objects.all()
    results = Product.objects.all()

    # Template
    template = "product_shop/search_product.html"

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
        "results": results,
        "query": query,
        "categories": categories,
        }

    return render(request, template, context)

@login_required
def add_product(request):
    """
    Search and return the data after filtering by query

    Parameters:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Rendered HTML to home page
        Add new data into database
    """

    # Identified the user seller or not
    if request.user.role != "SELLER":
        return HttpResponseForbidden("Only Seller can add product")

    # Templates
    template = "product_shop/add_product.html"

    # Add form to add the product
    form = AddProductForm()
    if request.method == "POST":
        # Add the form
        form = AddProductForm(request.POST, request.FILES)
        images = request.FILES.getlist("images")

        # Check the forms valid or not
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            # Save the image
            for image in images:
                ProductImage.objects.create(product=product, image=image)

        return redirect('base:home')

    # Add context for django template
    context = {"form": form}

    # Render the result
    return render(request, template, context)

@login_required
def edit_product(request, pk):
    """
    Edit data existing product by primary key

    Parameters:
        request (HttpRequest): The HTTP request object
        pk (int): Primary key

    Returns:
        HttpResponse: Rendered HTML to home page
        Save editting data product
    """
    if request.user.role != "SELLER":
        return HttpResponseForbidden("Only Seller can edit data product")

    # Templates
    product = get_object_or_404(Product, id=pk)
    # template = "product_shop/edit_product.html"
    template = "product_shop/add_product.html"

    # Process the edit data if method is POST
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_shop:product_detail", product=product.id)

    context = {"form": form}
    return render(request, template, context)

@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("base:home")
    else:
        form = CategoryForm()

    template = "product_shop/add_category.html"
    context = {
        "form": form,
    }
    return render(request, template, context)
