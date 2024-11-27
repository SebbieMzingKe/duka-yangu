from cart.cart import Cart
from django.shortcuts import redirect, render

from .forms import OrderCreatedForm
from .models import OrderItem
from .tasks import order_created

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreatedForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )


            # clear the cart
            cart.clear()

            # launch asynchronous 
            order_created.delay(order.id)
            
            # set order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('payments:process')
    else:
        form = OrderCreatedForm()
    return render(
        request,
        'orders/order/create.html',
        {
            'cart': cart,
            'form': form
        }

    )