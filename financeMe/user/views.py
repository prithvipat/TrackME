from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.models import Profile, Transactions, Subscriptions, Budget
import os
from datetime import date, timedelta
import pandas as pd
import csv
this_year = date.today().year
this_month = date.today().month
this_day = date.today().day

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

    Date,Category,Retailer,Amount,
"""

"""
def temp(profile):
    # - figure out how to allow user to create the folder and allow accept the download or not
    # - Allow user to download all csv files from settings page
    if this_month >= 8:
        exsisting_csv = CSVFiles.objects.filter(profile=profile, csvfile__icontains=f"{date.today().year}_Report.csv")
        prev_year_transactions = Transactions.objects.filter(profile=profile, date__year=date.today().year)

        if not exsisting_csv:
            data = {
                'Date': [],
                'Category': [],
                'Retailer': [],
                'Amount': []
            }

            for i in prev_year_transactions:
                data['Date'].append(str(i.date))
                data['Category'].append(i.category)
                data['Retailer'].append(i.retailer)
                data['Amount'].append(f"${i.amount}")

            df = pd.DataFrame(data)
            new_file = df.to_csv(index=True)
            file_name = f"{this_year}_Report.csv"

            new_csv = CSVFiles.objects.create(profile=profile)
            new_csv.csvfile.save(file_name, new_csv)
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

def setBudget(request, profile):
    
    budget = request.POST['amount']
    category = request.POST['category']
    current_budget = Budget.objects.filter(profile=profile, category=category).exists()


    if not current_budget:
        all_budgets = Budget.objects.filter(profile=profile)
        total = 0

        for i in all_budgets:
            total += i.set_amount
        
            if total < profile.cash_flow:
                new_budget = Budget.objects.create(profile=profile, category=category, set_amount=budget)
                new_budget.save()

            elif total >= profile.cash_flow:
                return "message"
    
    return 'Good'

def displayBudget(profile):
    budgets = Budget.objects.filter(profile=profile)


def compare_budget():
    pass


def bar_graph_data(profile): # to check and get data from current year
    all_transaction = Transactions.objects.filter(profile=profile, date__year=this_year).order_by('-time') # Geting data from current year
    months = {'Jan': 0,'Feb': 0,'Mar': 0,'Apr': 0,'May': 0,'Jun': 0,'Jul': 0,'Aug': 0,'Sept': 0,'Oct':0,'Nov':0,'Dec': 0}

    if len(all_transaction) == 0:
        return months
    
    else:
        for i in all_transaction: # Lazy code :( need to fix
            if i.date.month == 1:
                months['Jan'] += i.amount
            
            if i.date.month == 2:
                months['Feb'] += i.amount
            
            if i.date.month == 3:
                months['Mar'] += i.amount

            if i.date.month == 4:
                months['Apr'] += i.amount

            if i.date.month == 5:
                months['May'] += i.amount

            if i.date.month == 6:
                months['Jun'] += i.amount

            if i.date.month == 7:
                months['Jul'] += i.amount

            if i.date.month == 8:
                months['Aug'] += i.amount

            if i.date.month == 9:
                months['Sept'] += i.amount

            if i.date.month == 10:
                months['Oct'] += i.amount

            if i.date.month == 11:
                months['Nov'] += i.amount

            if i.date.month == 12:
                months['Dec'] += i.amount

        return months

def pie_graph_data(user_transactions):
    total = 0
    dicts = {
        'Food': 0,
        'Transportation': 0,
        'Clothing': 0,
        'Utilities': 0,
        'Vacation': 0,
        'Others': 0   
        }
    
    if len(user_transactions) != 0:
        for i in user_transactions: # To add the amount made to each
            dicts[i.category] += i.amount
            total += i.amount
        
        for n in dicts:
            dicts[n] /= total
            dicts[n] *= 100
            dicts[n] = round(dicts[n])
        
        return dicts
    
    else:
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
        dicts = pie_graph_data(user_transactions)
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

    if request.method == 'POST':
        msg = setBudget(request, profile)

        if msg == 'Good':
            messages.info(request, 'Budget Saved')
        
        if msg == 'message':
            messages.info(request, 'Budget over cashflow')


    return render(request, 'settings.html', {'profile': profile})

@login_required(login_url='login')
def make_transaction(request):

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'Transaction': # To add a transaction
            profile = request.user.username
            categoryNum = request.POST['category']
            category = CATEGORY_CHOICES[int(categoryNum)-1]
            amount = request.POST['amount']
            retailer = request.POST['retailer']
            new_transaction = Transactions.objects.create(profile=profile, category=category, amount=amount, retailer=retailer)
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
    user_transactions = Transactions.objects.filter(profile=profile, date__month=date.today().month).order_by('-time')
    user_transactions_length = len(user_transactions)
    user_subscriptions = Subscriptions.objects.filter(profile=profile)
    user_subscriptions_length = len(user_subscriptions)
    dicts = pie_graph_data(user_transactions)
    yearly = bar_graph_data(profile)
    budgets = Budget.objects.filter(profile=profile)

    context = {
        "username": profile,
        "num_transactions": user_transactions_length,
        "transactions": user_transactions,
        'categories': dicts,
        'subscriptions': user_subscriptions,
        'num_subscriptions': user_subscriptions_length,
        'yearly': yearly,
        'year': date.today().year,
        'budget': budgets
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
