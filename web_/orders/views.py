from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Product, OrderItem, Cart, CartItem, InsufficientStockError
from .forms import OrderForm
from django.db.models import Sum, Count
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

def checkout(request):
    user_cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    cart_items = CartItem.objects.filter(cart=user_cart)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            for cart_item in cart_items:
                if cart_item.count > cart_item.product.stock:
                    # Если запрошенное количество больше, чем в stock, вызываем ошибку
                    raise ValidationError(f"Insufficient stock for product {cart_item.product.name}")





            # Создаем заказ
            order = form.save(commit=False)
            order.save()

            # Создаем позиции заказа
            for cart_item in cart_items:
                try:

                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        count=cart_item.count,
                        discount=cart_item.discount,
                        cost=cart_item.cost
                    )
                except InsufficientStockError as e:
                    # Обработка случая, когда запас товара меньше заказанного количества
                    # Можно вывести ошибку или принять другие меры
                    print(f"Error: {e}")

            # Очищаем корзину после оформления заказа
            user_cart.products.clear()

            return redirect('order_success')

    else:
        form = OrderForm(initial={'type': 'online', 'status': 'active'})

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items})

def order_success(request):
    return render(request, 'order_success.html')


def view_cart(request):
    session_key = request.session.session_key
    user_cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_items = CartItem.objects.filter(cart=user_cart)
    return render(request, 'cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    user_cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    if not item_created:
        cart_item.count += 1
        cart_item.save()
    return redirect('index')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    user_cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_item = get_object_or_404(CartItem, cart__session_key=session_key, product=product)
    cart_item.delete()
    return redirect('view_cart')

def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    user_cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_item = get_object_or_404(CartItem, cart__session_key=session_key, product=product)

    if request.method == 'POST':
        count = request.POST.get('count')
        if count.isdigit() and 0 < int(count) <= product.stock:
            cart_item.count = int(count)
            cart_item.save()
        else:
            
            pass

    return redirect('view_cart')

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})



def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'order_form.html', {'form': form})

def order_edit(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_form.html', {'form': form})

def order_report(request):
    date = request.GET.get('date')

    if not date:
        return HttpResponseBadRequest("Date parameter is required.")

    try:
        completed_orders = Order.objects.filter(completed_at__date=date, status='completed')
        total_cost = completed_orders.aggregate(Sum('orderitem__cost'))['orderitem__cost__sum'] or 0
        order_count = completed_orders.count()
    except ValueError:
        return HttpResponseBadRequest("Invalid date format.")

    return render(request, 'order_report.html', {'date': date, 'total_cost': total_cost, 'order_count': order_count})
