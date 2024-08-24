from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.models import Profile, Transactions, Subscriptions
import os
from datetime import date, timedelta

this_year = date.today().year
this_month = date.today().month

CATEGORY_CHOICES = ['Food','Transportation', 'Clothing', 
                    'Utilities','Vacation', 'Others']
"""
def change_balance(profile, amount):
    if profile.balance >= int(amount):
        profile.balance -= int(amount)
        return True
        # if balance <= 100 send message
    
    else:
        return False
"""
def check_yearly_spending(profile):
    all_transaction = Transactions.objects.filter(profile=profile, date__year=this_year)
    all_subscriptions = Subscriptions.filter(profile=profile)

    total = 0
    total_subscription = 0

    for i in all_transaction:
        total += i.amount
    
    for x in all_subscriptions:
        total_subscription = total_subscription + (i.price * 12)
    
    return total, total_subscription

def bar_graph_data(profile): # to check and get data from current year
    all_transaction = Transactions.objects.filter(profile=profile, date__year=this_year).order_by('-time') # Geting data from current year
    years = {'Jan': 0,'Feb': 0,'Mar': 0,'Apr': 0,'May': 0,'Jun': 0,'Jul': 0,'Aug': 0,'Sept': 0,'Oct':0,'Nov':0,'Dec': 0}

    for i in all_transaction: # Lazy code :( need to fix
        if i.date.month == 1:
            years['Jan'] += i.amount
        
        if i.date.month == 2:
            years['Feb'] += i.amount
        
        if i.date.month == 3:
            years['Mar'] += i.amount

        if i.date.month == 4:
            years['Apr'] += i.amount

        if i.date.month == 5:
            years['May'] += i.amount

        if i.date.month == 6:
            years['Jun'] += i.amount

        if i.date.month == 7:
            years['Jul'] += i.amount

        if i.date.month == 8:
            years['Aug'] += i.amount

        if i.date.month == 9:
            years['Sept'] += i.amount

        if i.date.month == 10:
            years['Oct'] += i.amount

        if i.date.month == 11:
            years['Nov'] += i.amount

        if i.date.month == 12:
            years['Dec'] += i.amount

    return years

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

        for i in user_transactions: # To add the amount made to each
            if i.category in CATEGORY_CHOICES:
                dicts[i.category] += i.amount
                total += i.amount
        
        for n in dicts:
            dicts[n] /= total
            dicts[n] *= 100
            dicts[n] = round(dicts[n])
        
        return dicts

@login_required(login_url='login')
def index(request):
    profile = request.user.username
    user = request.user
    user_transactions = Transactions.objects.filter(profile=profile, date__year=date.today().year).order_by('-time')
    latest = ''
    second = ''
    dicts  = {}
    user_object = Profile.objects.get(user=user) # More lazy code, but to check if there are any transactions if there are none show none else show all of them

    if len(user_transactions) == 0:
        return render(request, 'index.html', {'profile': profile, 'categories': dicts, 'user':user_object, 'latest':latest, 'second':second})
    
    else:
        dicts = get_categories(user_transactions)
        latest = user_transactions[0]
        if len(user_transactions) > 1:
            second = user_transactions[1]

        return render(request, 'index.html', {'profile': profile, 'categories': dicts, 'user':user_object, 'latest':latest, 'second':second})

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def settings(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)

    return render(request, 'settings.html', {'profile': profile})

@login_required(login_url='login')
def make_transaction(request):

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'Transaction': # To add a transaction
            profile = request.user.username
            transaction_type =  True
            categoryNum = request.POST['category']
            category = CATEGORY_CHOICES[int(categoryNum)-1]
            amount = request.POST['amount']
            retailer = request.POST['retailer']
            new_transaction = Transactions.objects.create(profile=profile, transaction_type=transaction_type, category=category, amount=amount, retailer=retailer)
            new_transaction.save()
            return redirect('/')
    
        if action == 'Subscription': # To add a Subscription
            profile = request.user.username
            amount = request.POST['amount']
            organization = request.POST['organization']

            if Subscriptions.objects.filter(profile=profile, organization=organization).exists():
                messages.info(request,f'You already have a {organization} subscription')
                return redirect('transactions')
            
            else:
                new_subscription = Subscriptions.objects.create(profile=profile, price=amount, organization=organization)
                new_subscription.save()
                return redirect('/')
    
    return render(request, 'transaction.html')

@login_required(login_url='login')
def check_transactions(request):
    profile = request.user.username
    user_transactions = Transactions.objects.filter(profile=profile, date__year=date.today().year).order_by('-time')
    user_transactions_length = len(user_transactions)
    user_subscriptions = Subscriptions.objects.filter(profile=profile)
    user_subscriptions_length = len(user_subscriptions)

    if len(user_transactions) == 0:
        return render(request, 'empy.html')

    else:
        dicts = get_categories(user_transactions)
        yearly = bar_graph_data(profile)
    
    context = {
        "username": profile,
        "num_transactions": user_transactions_length,
        "transactions": user_transactions,
        'categories': dicts,
        'subscriptions': user_subscriptions,
        'num_subscriptions': user_subscriptions_length,
        'yearly': yearly,
        'year': date.today().year
    }

    if request.method == 'POST':
        pass

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
