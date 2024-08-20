from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.models import Profile, Transactions
from django.http import HttpResponse, JsonResponse
import os

def get_categories(user_transactions):
        total = 0
        dicts = {
            'Food': 0,
            'Transportation': 0,
            'Clothing': 0,
            'Utilities': 0,
            'Vacation': 0,
            'Others': 0
        }

        for i in user_transactions:
            if i.category in CATEGORY_CHOICES:
                dicts[i.category] += i.amount
                total += i.amount
        
        for n in dicts:
            dicts[n] /= total
            dicts[n] *= 100
            dicts[n] = round(dicts[n])
        
        return dicts

CATEGORY_CHOICES = ['Food','Transportation', 'Clothing', 
                    'Utilities','Vacation', 'Others']

@login_required(login_url='login')
def index(request):
    profile = request.user.username
    user = request.user
    user_transactions = Transactions.objects.filter(profile=profile).order_by('-date')
    dicts = get_categories(user_transactions)
    user_object = Profile.objects.get(user=user)

    return render(request, 'index.html', {'profile': profile, 'categories': dicts, 'user':user_object})

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def settings(request):
    return render(request, 'settings.html')

@login_required(login_url='login')
def make_transaction(request):

    if request.method == 'POST':
        profile = request.user.username
        transaction_type =  True
        categoryNum = request.POST['category']
        category = CATEGORY_CHOICES[int(categoryNum)-1]
        amount = request.POST['amount']
        date = request.POST['date']
        retailer = request.POST['retailer']

        new_transaction = Transactions.objects.create(profile=profile, transaction_type=transaction_type, category=category, amount=amount, date=date, retailer=retailer)
        new_transaction.save()

        return redirect('/')
    
    else:
        return render(request, 'transaction.html')

@login_required(login_url='login')
def check_transactions(request):
    profile = request.user.username
    user_transactions = Transactions.objects.filter(profile=profile).order_by('-date')
    user_transactions_length = len(user_transactions)

    dicts = get_categories(user_transactions)

    
    context = {
        "username": profile,
        "num_transactions": user_transactions_length,
        "transactions": user_transactions,
        'categories': dicts,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
                
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']

        if password == password2:
                
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
        
            else:

                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect('index')

        else:
            messages.info(request, 'Passwords do not Match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')