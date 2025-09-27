from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from website.models import Product, AuthUser
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# -------------------------
# Home page
# -------------------------
def home(request):
    products = Product.objects.all()
    return render(request, 'website/index.html', {'products': products})

# -------------------------
# Search page
# -------------------------
def search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    context = {
        'title': 'Search - My Shop',
        'description': 'Find the perfect product.',
        'products': products
    }
    return render(request, 'website/index.html', context=context)

# -------------------------
# Products page (login required)
# -------------------------
@login_required(login_url='login')
def products_page(request):
    products = Product.objects.all()
    return render(request, 'website/product_list.html', {'products': products})

# -------------------------
# Product detail page (login required)
# -------------------------
@login_required(login_url='login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'website/product_detail.html', {'product': product})

# -------------------------
# Product API
# -------------------------
@csrf_exempt
def product_list(request, product_id=None):
    if request.method == "GET":
        products = Product.objects.all().values('id', 'name', 'description', 'price', 'stock', 'image')
        # include image url in API response
        products_list = []
        for p in products:
            p['image'] = request.build_absolute_uri('/media/' + p['image'])
            products_list.append(p)
        return JsonResponse(products_list, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                stock=data['stock']
                # Image upload via API not included here
            )
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'message': 'Product created successfully!'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == "PUT" and product_id:
        try:
            data = json.loads(request.body)
            product = Product.objects.get(pk=product_id)
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.stock = data.get('stock', product.stock)
            product.save()
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'message': 'Product updated successfully!'
            })
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# -------------------------
# Signup
# -------------------------
def signup_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password2')

        if AuthUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        if AuthUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        user = AuthUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'website/signup.html')

# -------------------------
# Login
# -------------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'website/login.html')

# -------------------------
# Logout
# -------------------------
def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

# -------------------------
# Profile page (login required)
# -------------------------
@login_required(login_url='login')
def profile(request):
    return render(request, 'website/include/profile.html', {'user': request.user})

# -------------------------
# Cart (login required)
# -------------------------
@login_required(login_url='login')
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, "Product added to cart!")
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Product removed from cart!")
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'website/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# -------------------------
# Checkout (login required)
# -------------------------
@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Your cart is empty!")
        return redirect('cart')

    products = Product.objects.filter(id__in=cart.keys())
    total_price = sum(product.price * cart[str(product.id)] for product in products)
    cart_items = [{'product': p, 'quantity': cart[str(p.id)]} for p in products]

    return render(request, 'website/checkout.html', {'cart_items': cart_items, 'total_price': total_price})
