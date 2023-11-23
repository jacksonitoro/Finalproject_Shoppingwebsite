from django.shortcuts import render, redirect, get_object_or_404
from davinshop.models import Product
from . models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from order.models import Order, OrderItem

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
                cart_id= _cart_id(request)       
            )
        cart.save(),
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
        cart_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request): #total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
        counter = sum(cart_item.quantity for cart_item in cart_items)
    except ObjectDoesNotExist:
        cart_items = []
        total = 0
        counter = 0


    #     for cart_item in cart_items:
    #         total += (cart_item.product.price * cart_item.quantity)
    #         counter += cart_item.quantity
    # except ObjectDoesNotExist:
    #     pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))

def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

        #creating order
        order = Order.objects.create(
            total = total,
            emailAddress=request.user.email,
        )

        #create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                product = cart_item.product.name,
                quantity = cart_item.quantity,
                price = cart_item.product.price,
                order = order
            )

        #Clear the cart after creating the order
        cart_items.delete()

        return render(request, 'orders/order_detail.html', {'order': order})
    except ObjectDoesNotExist:
        return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail') 