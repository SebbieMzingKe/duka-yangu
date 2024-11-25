from django.shortcuts import get_object_or_404, render
from .models import Category, Product


# Create your views here.


def product_list(request, category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)

    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        return render(
            request,
            'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
        )
    
# retrieve and display a single product
def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id = id, slug = slug, available = True
            )

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
        }
    )