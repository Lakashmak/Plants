from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django import forms
from django.http import HttpResponseRedirect, HttpRequest
from django.db.models import Q
from django.db.models.functions import Lower
import hashlib
from .models import Product, User, Order, OrderProduct
from .forms import ContactForm, LoginForm


# Create your views here.                                  11)Сад и огород              о нас

def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', context={
        'title' : 'Plants',
        'name' : 'catalog',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'products' : products,
    })

def product_page(request, id):
    product = Product.objects.get(id=id)
    product1 = Product.objects.get(id=id)
    return render(request, 'product_page.html', context={
        'title' : 'Страница товара',
        'name' : 'product_page',
        'link' : '../../',
        'user_id' : request.session.get('user_id'),
        'product' : product,
        'product1' : product1,
    })

def basket(request):
    if 'basket' not in request.session: request.session['basket'] = {} #request.session.clear() request.session.save()
    if request.method == 'POST': #return redirect('info', request.POST)
        if any(key.startswith('shop[') for key in request.POST):
            quantity = int(request.POST['quantity'])
            product_id = next((key.split('[')[1].split(']')[0] for key in request.POST if key.startswith('shop[')), None)
            if product_id in request.session['basket']: request.session['basket'][product_id] += quantity
            else: request.session['basket'][product_id] = quantity
            if quantity <= 0: del request.session['basket'][product_id]
            request.session.save()
            return redirect('basket')
        if any(key.startswith('quantity[') for key in request.POST):
            product_id = next((key.split('[')[1].split(']')[0] for key in request.POST if key.startswith('quantity[')), None)
            quantity = int(request.POST.get(f'quantity[{product_id}]', 0))
            request.session['basket'][product_id] = quantity
            if quantity <= 0: del request.session['basket'][product_id]
            request.session.save()
            return redirect('basket')
    if len(request.session['basket']) == 0: return redirect('info', 'Корзина пуста!')
    product_ids = request.session['basket'].keys() #.get('basket', {}).keys()
    products = Product.objects.filter(id__in=product_ids) # product = Product.objects.get(id=product_id)
    basket_data = []
    for product in products:
        quantity = request.session['basket'].get(str(product.id), 0)
        basket_data.append({'product': product, 'quantity': quantity})
    return render(request, 'basket.html', context={
        'title' : 'Корзина',
        'name' : 'basket',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'products' : products,
        'basket_data' : basket_data,
    })

def search(request):
    if request.method == 'GET':
        message = request.GET['search']
        if not message == '':
            products = Product.objects.filter(name__icontains = message) #    Lower('name').contains(message.lower())
        else:
            message = 'Введён пустой запрос!'
            products = Product.objects.all()
    return render(request, 'search.html', context={
        'title' : 'Результаты поиска',
        'name' : 'search',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'products' : products,
        'request' : message,
    })

def registration(request: HttpRequest):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            password_hash = hashlib.sha256(str(password).strip().encode()).hexdigest()
            user = User(name=name, status=0, phone_number=phone, email=email, delivery_address=address, password_hash=password_hash) # .objects.create
            user.save()
            request.session['user_id'] = user.id #login(request, user)
            return redirect('personal_area') # HttpResponseRedirect('/personal_area/')
    else:
        form = ContactForm()
    return render(request, 'registration.html', context={
        'title' : 'Регистрация',
        'name' : 'registration',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'form' : form,
    })

def personal_area(request):
    user = None
    if request.session.get('user_id'):
        user = User.objects.get(id=request.session.get('user_id'))
    if request.method == 'POST':
        if 'exit' in request.POST:
            del request.session['user_id'] #logout(request)
            return redirect('login_page')
        if 'delete' in request.POST:
            del request.session['user_id']
            user.delete()
            return redirect('info', 'Аккаунт удалён!')
            #HttpResponseRedirect('/personal_area/')
        #if 'admin' in request.POST:
        #if 'button' in request.POST:
            #form = ContactForm(request.POST)
    #else:
        #form = ContactForm()
    return render(request, 'personal_area.html', context={
        'title' : 'Личный кабинет',
        'name' : 'personal_area',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'user' : user,
        # 'form' : form,
    })

def login_page(request: HttpRequest):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_ = form.cleaned_data['login']
            user = User.objects.filter(Q(phone_number=login_) | Q(email=login_)).first()
            if user is not None:
                request.session['user_id'] = user.id #login(request, user)
                return redirect('personal_area') # HttpResponseRedirect('/personal_area/')
    else:
        form = LoginForm()
    return render(request, 'login_page.html', context={
        'title' : 'Вход',
        'name' : 'login_page',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'form' : form,
    })

def info(request, massange):
    return render(request, 'base.html', context={
        'title' : massange,
        'name' : 'info',
        'link' : '../../',
        'user_id' : request.session.get('user_id'),
        'massange' : massange,
    })

def checkout_page(request):
    if 'basket' not in request.session: request.session['basket'] = {}
    if len(request.session['basket']) == 0: return redirect('info', 'Корзина пуста!')
    if 'user_id' not in request.session: return redirect('login_page')
    user = User.objects.get(id=request.session['user_id'])
    product_ids = request.session['basket'].keys()
    basket_data = []
    summ = 0
    for product_id in product_ids:
        quantity = request.session['basket'].get(str(product_id), 0)
        basket_data.append({'product_id': product_id, 'quantity': quantity})
        summ += int(Product.objects.get(id=product_id).price * quantity)
    if request.method == 'POST':
        if 'btn' in request.POST and 'pay' in request.POST:
            pay = request.POST['pay']
            order = Order(user=user, payment_method=pay, status=0)
            order.save()
            for data in basket_data:
                product = Product.objects.get(id=data['product_id'])
                quantity = data['quantity']
                orderProduct = OrderProduct(order=order, product=product, quantity=quantity)
                orderProduct.save()
            del request.session['basket']
            request.session.save()
            return redirect('info', 'Заказ оформлен!')
    return render(request, 'checkout_page.html', context={
        'title' : 'Оформление заказа',
        'name' : 'checkout_page',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'summ' : summ
    })

def order_list(request):
    if 'user_id' not in request.session: return redirect('login_page')
    if request.method == 'POST':
        if any(key.startswith('delete[') for key in request.POST):
            order_id = next((key.split('[')[1].split(']')[0] for key in request.POST if key.startswith('delete[')), None)
            order = Order.objects.get(id=order_id)
            order.delete()
            return redirect('order_list')
        if any(key.startswith('repeat[') for key in request.POST):
            order_id = next((key.split('[')[1].split(']')[0] for key in request.POST if key.startswith('repeat[')), None)
            order = Order.objects.get(id=order_id)
            if 'basket' in request.session: del request.session['basket']
            request.session['basket'] = {}
            for orderProduct in OrderProduct.objects.filter(order=order):
                product_id = orderProduct.product.id
                request.session['basket'][product_id] = orderProduct.quantity
            request.session.save()
            return redirect('basket')
    orders = Order.objects.filter(user=User.objects.get(id=request.session.get('user_id')))
    orders_data = []
    for order in orders:
        order_id = order.id
        pay = order.payment_method
        dete = order.date
        status = order.status
        products = []
        summ = 0
        for orderProduct in OrderProduct.objects.filter(order=order):
            quantity = orderProduct.quantity
            name = orderProduct.product.name
            price = orderProduct.product.price
            priceS = price * quantity
            summ += priceS
            products.append({'name': name, 'price': price, 'quantity': quantity, 'priceS': priceS,})
        orders_data.append({'id': order_id, 'dete': dete, 'pay': pay, 'summ': summ, 'status': status, 'products': products,})
    return render(request, 'order_list.html', context={
        'title' : 'Список заказов',
        'name' : 'order_list',
        'link' : '../',
        'user_id' : request.session.get('user_id'),
        'orders_data': orders_data
    })