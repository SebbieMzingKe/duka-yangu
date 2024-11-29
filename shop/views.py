from django.shortcuts import get_object_or_404, render

from .recommender import Recommender
from .models import Category, Product
from cart.forms import CartAddProductForm


# Create your views here.


def product_list(request, category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)

    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category, 
            translations__language_code = language,
            translations__slug = category_slug
        )
    
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
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product, 
        translations__language_code = language,
        id = id, 
        translations__slug = slug, available = True
            )

    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)


    print(f"Recommended products for {product}: {recommended_products}")
    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products
        }
    )