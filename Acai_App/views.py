from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Acai, Order
import bcrypt, random

def main(request):
    if request.session.get('user_id'):
        context = {
            'user': User.objects.get(id=request.session['user_id']),
        }
    context = {

    }
    return render(request, 'main.html', context)

def contact_page(request):
    return render(request, 'contact.html')

def login_page(request):
    return render(request, 'login.html')

def account_page(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'user_orders': Order.objects.filter(user_id=request.session['user_id'])
    }
    return render(request, 'account.html', context)

def order_page(request):
    if 'user_id' not in request.session:
        return redirect('/login_page')
    return render(request, 'order.html')

def story_page(request):
    return render(request, 'story.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/main')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/account')

def build(request):
    return render(request, 'build.html')

def create_bowl(request):
    toppings =[]
    if request.POST.get("Blueberry"):
        toppings.append(request.POST["Blueberry"])
    if request.POST.get("Strawberry"):
        toppings.append(request.POST["Strawberry"])
    if request.POST.get("Honey"):
        toppings.append(request.POST["Honey"])
    if request.POST.get("Chia Seeds"):
        toppings.append(request.POST["Chia Seeds"])
    if request.POST.get("Banana"):
        toppings.append(request.POST["Banana"])
    if request.POST.get("Almond Butter"):
        toppings.append(request.POST["Almond Butter"])
    if request.POST.get("Peanut Butter"):
        toppings.append(request.POST["Peanut Butter"])
    if request.POST.get("Chocolate chunks"):
        toppings.append(request.POST["Chocolate chunks"])
    if request.POST.get("Caramel syrup"):
        toppings.append(request.POST["Caramel syrup"])
    user = Acai.objects.create(
        method = request.POST['method'],
        size = request.POST['size'],
        base = request.POST['base'],
        quantity = request.POST['quantity'],
        toppings = toppings,
        beverage = request.POST["beverage"]
    )
    id=user.id
    return redirect(f'/receipt/{id}')

def order_again(request, id):
    previous_order = Order.objects.get(id=id)
    new_order = Acai.objects.create(
        method = previous_order.acai.method,
        size = previous_order.acai.size,
        base = previous_order.acai.base,
        quantity = previous_order.acai.quantity,
        beverage = previous_order.acai.beverage,
        toppings = previous_order.acai.toppings
    )
    # print(type(previous_order.toppings))
    # for t in previous_order.toppings:
    #     new_order.toppings.add(t)
    Order.objects.create(acai=new_order, amount=previous_order.amount, user=previous_order.user)
    id=new_order.id
    return redirect(f'/receipt/{id}')

def re_order_page(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'user_orders': Order.objects.filter(user_id=request.session['user_id'])
    }
    user = context['user']
    user_orders = context['user_orders']
    print(f'user: {user}, user_orders: {user_orders}')
    return render(request, 're_order.html', context)

def receipt(request, id):
    bowl_created=Acai.objects.get(id=id)
    quantity=bowl_created.quantity
    print(quantity)
    price=0
    if bowl_created.size=='Small':
        price+=6*quantity
    elif bowl_created.size=='Medium':
        price+=8*quantity
    elif bowl_created.size=='Large':
        price+=10*quantity
    bev_price_list = {
        "none": 0,
        "None": 0,
        "Bottled Water": 2,
        "Yerba Mate": 3,
        "Matcha Tea": 3,
        "Sparkling Water": 4,
        "Kombucha": 5,
    }
    price+=bev_price_list[bowl_created.beverage]
    request.session['bowl']=bowl_created.id
    request.session['price']=price
    context = {
        'new_bowl':bowl_created,
        'total':price
    }
    return render(request, 'receipt.html', context)

def purchase(request):
    bowl=Acai.objects.get(id=request.session['bowl'])
    price=request.session['price']
    user=User.objects.get(id=request.session['user_id'])
    Order.objects.create(acai=bowl, amount=price, user=user)
    
    return redirect('/purchase_page')

def purchase_page(request):
    context = {
        'order':Order.objects.last()
    }

    return render(request, 'purchase.html', context)

def surprise(request):
    first=Acai.objects.first()
    last=Acai.objects.last()
    acai_id=random.randint(first.id,last.id)
    acai=Acai.objects.get(id=acai_id)
    context = {
        'acai':acai
    }

    return render(request, 'surprise.html', context)

def update_user(request, id):
    print('HERE')
    print(id)
    errors = User.objects.edit_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/account')
    user = User.objects.get(id=id)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('/account')


def logout(request):
    request.session.flush()

    return redirect('/')