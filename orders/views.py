from cart.cart import Cart
from django.shortcuts import render
from .forms import OrderCreatedForm
from .models import OrderItem

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreatedForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objeects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )


            # clear the cart
                cart.clear()
                return render(
                    request,
                    'orders/order/created.httml',
                    {
                        'order': order
                    }
                )
        else:
            form = OrderCreatedForm()
        return render(
            request,
            'orders/order/create.httml',
            {
                'cart': cart,
                'form': form
            }

        )