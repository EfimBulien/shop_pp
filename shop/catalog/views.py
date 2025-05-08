from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Product, Category, Tag, Order, OrderItem
from .forms import ProductForm, CategoryForm, OrderForm
from datetime import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

def index(request):
    return render(request, 'catalog/index.html')

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(is_deleted=False)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category, is_deleted=False)
    return render(request, 'catalog/category_products.html', {'category': category, 'products': products})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'catalog/add_category.html', {'form': form})

class TagListView(ListView):
    model = Tag
    template_name = 'catalog/tag_list.html'
    context_object_name = 'tags'

def tag_products(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    products = tag.product_set.filter(is_deleted=False)
    return render(request, 'catalog/tag_products.html', {'tag': tag, 'products': products})

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    
    for product_id, item in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        quantity = item['quantity']
        products.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity
        })
        total_price += product.price * quantity
    
    return render(request, 'catalog/cart.html', {
        'products': products,
        'total_price': total_price
    })


@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=product_id)
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'quantity': 1,
            'price': str(product.price)
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': sum(item['quantity'] for item in cart.values()),
            'message': f'Товар "{product.name}" добавлен в корзину'
        })
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    
    return redirect('cart_view')

def create_order(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, "Ваша корзина пуста")
        return redirect('product_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.number = f"ORD-{timezone.now().strftime('%Y%m%d-%H%M%S')}"
            order.save()
            
            for product_id, item in cart.items():
                product = Product.objects.get(pk=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    discount_per_item=0
                )
            del request.session['cart']
            messages.success(request, f"Ваш заказ №{order.number} успешно оформлен!")
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'catalog/create_order.html', {
        'form': form,
        'cart': cart
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'catalog/order_success.html', {'order': order})