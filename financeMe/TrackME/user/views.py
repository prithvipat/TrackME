from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.models import Profile, Transactions, Subscriptions
import os
from datetime import date, timedelta
import pandas as pd
import csv
this_year = date.today().year
this_month = date.today().month
this_day = date.today().day


all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
CATEGORY_CHOICES = ['Food','Transportation', 'Clothing', 'Utilities','Vacation', 'Others']
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


def get_budgets(profile, user_transactions):
    food = profile.food_budget
    util = profile.utilities_budget
    others = profile.others_budget
    clothes = profile.clothing_budget
    transport = profile.transport_budget
    
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

    return (food, util, others, clothes, transport, dicts)

def store_distribution(transactions):
    pass

def check_yearly_spending(all_transaction, all_subscriptions, monthly_spend): #Checks yearly spending on transactions + subscriptions + combined

    total = 0
    total_subscription = 0
    monthly_spending = 0
    monthly_subs = 0

    for i in all_transaction:
        total += i.amount
    
    for n in monthly_spend:
        monthly_spending += n.amount

    for x in all_subscriptions:
        total_subscription = total_subscription + (x.price * 12)
        monthly_subs += x.price
    
    everything = total + total_subscription
    
    return total,total_subscription, monthly_spending, monthly_subs,everything

def setBudget(request, profile): # WIP Sets a budget or edits budget

    category = request.POST.get('category')
    category = category.lower()
    amount = request.POST.get('amount')

    return profile.food_budget

def recent_stores(transactions): # Gets current month transactions
    le = len(transactions)
    stores_count = {}

    for i in transactions:
        if i.retailer in stores_count:
            stores_count[i.retailer] += 1
        
        else:
            stores_count.update({i.retailer: 1})
    
    for i in stores_count:
        stores_count[i] = (stores_count[i]/le) * 100
    
    return stores_count

def bar_graph_data(transactions): # to check and get data from current year
    months = {'Jan': 0,'Feb': 0,'Mar': 0,'Apr': 0,'May': 0,'Jun': 0,'Jul': 0,'Aug': 0,'Sept': 0,'Oct':0,'Nov':0,'Dec': 0}

    if len(transactions) == 0:
        return months
    
    else:
        for i in transactions: # Lazy code :( need to fix
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

def pie_graph_data(user_transactions): # Gets data for Pie chart
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
def index(request): # Main page
    profile = request.user.username
    user = request.user
    user_transactions = Transactions.objects.filter(profile=profile, date__month=date.today().month).order_by('-time')
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
    profile = request.user.username  # Profile Username
    user_object = User.objects.get(username=profile)  # Get the user model
    profile_model = Profile.objects.get(user=user_object)  # Get the profile model

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'budgets':

            # Get the values from the form, set a default of None if a field is empty
            new_food_budget = request.POST.get('food', None)
            new_clothing_budget = request.POST.get('clothes', None)
            new_util_budget = request.POST.get('util', None)
            new_transport_budget = request.POST.get('transport', None)
            new_others_budget = request.POST.get('others', None)

            # Update the budgets if they are valid
            if new_food_budget and new_food_budget.isdigit():
                profile_model.food_budget = int(new_food_budget)

            if new_clothing_budget and new_clothing_budget.isdigit():
                profile_model.clothing_budget = int(new_clothing_budget)

            if new_util_budget and new_util_budget.isdigit():
                profile_model.utilities_budget = int(new_util_budget)

            if new_transport_budget and new_transport_budget.isdigit():
                profile_model.transport_budget = int(new_transport_budget)
            
            if new_others_budget and new_others_budget.isdigit():
                profile_model.others_budget = int(new_others_budget)

            profile_model.save()

            return redirect('settings')

    else:
        context = {
            'food_budget': profile_model.food_budget,
            'clothing_budget': profile_model.clothing_budget,
            'utilities_budget': profile_model.utilities_budget,
            'transport_budget': profile_model.transport_budget,
            'others_budget': profile_model.others_budget,
        }

        return render(request, 'settings.html', context)

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
            return redirect('transactions')
    
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
                return redirect('transactions')

        if action == 'Reaccuring Transactions':
            profile = request.user.username
            purchase = request.POST['purchase']
            amount = request.POST['amount']

            

    
    return render(request, 'transaction.html')

@login_required(login_url='login')
def check_transactions(request):
    profile = request.user.username # Profile Username
    user_object = User.objects.get(username=profile) # Gets the user Model
    profile_model = Profile.objects.get(user=user_object) # Gets the profile Model
    user_transactions_month = Transactions.objects.filter(profile=profile, date__month=date.today().month).order_by('-time') # Transactions for the month
    user_transactions_year = Transactions.objects.filter(profile=profile, date__year=date.today().year) # Transactions for the year
    user_transactions_len_this_month = len(user_transactions_month) # Number of transactions this month
    user_subscriptions = Subscriptions.objects.filter(profile=profile) # All subscriptions
    user_subscriptions_length = len(user_subscriptions) # Number of subscriptions
    yearly = bar_graph_data(user_transactions_year) # Data for bar graph
    pie_graph = pie_graph_data(user_transactions_month) # Data for pie graph (current month)
    percentage_year = pie_graph_data(user_transactions_year) # Data for pie graph (year)
    total_year, total_subscription, total_monthly, monthly_subscription, total = check_yearly_spending(user_transactions_year, user_subscriptions, user_transactions_month)
    food, util, others, clothes, transport, this_dict = get_budgets(profile_model, user_transactions_month)

    context = {
        "username": profile, # Profile
        "transactions": user_transactions_month, # Transactions for the month
        'categories': pie_graph, # Pie graph data
        'subscriptions': user_subscriptions, # All subscriptions
        'num_subscriptions': user_subscriptions_length, # Number of subscriptions
        'bar_graph_data': yearly, # Total Year spending
        'this_month': all_months[this_month -1], # The month
        'this_year': this_year,
        'num_transactions': user_transactions_len_this_month,
        'total_year': total_year, # Total 
        'total_sub': total_subscription, # 
        'total_monthly': total_monthly, # 
        'monthly_subs': monthly_subscription, # Total spending for subscriptions
        'percentage_yearly': percentage_year,
        'food': food, 
        'util': util,
        'others': others, 
        'clothes': clothes,
        'transport': transport,
        'this_dicts': this_dict,
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
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
        
            else:

                user = User.objects.create_user(username=email, password=password, first_name=firstName, last_name=lastName)
                user.save()

                user_login = auth.authenticate(username=email, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=email)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect('index')

        else:
            messages.info(request, 'Passwords do not Match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def playground(request):
    profile = request.user.username  # Profile Username
    user_object = User.objects.get(username=profile)  # Get the user model
    profile_model = Profile.objects.get(user=user_object)  # Get the profile model

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'budget':

            # Get the values from the form, set a default of None if a field is empty
            new_food_budget = request.POST.get('food', None)
            new_clothing_budget = request.POST.get('clothes', None)
            new_util_budget = request.POST.get('util', None)
            new_transport_budget = request.POST.get('transport', None)

            # Update the budgets if they are valid
            if new_food_budget and new_food_budget.isdigit() and int(new_food_budget) > 0:
                profile_model.food_budget = int(new_food_budget)

            if new_clothing_budget and new_clothing_budget.isdigit() and int(new_clothing_budget) > 0:
                profile_model.clothing_budget = int(new_clothing_budget)

            if new_util_budget and new_util_budget.isdigit() and int(new_util_budget) > 0:
                profile_model.utilities_budget = int(new_util_budget)

            if new_transport_budget and new_transport_budget.isdigit() and int(new_transport_budget) > 0:
                profile_model.transport_budget = int(new_transport_budget)

            profile_model.save()

            return redirect('playground')

    else:
        context = {
            'food_budget': profile_model.food_budget,
            'clothing_budget': profile_model.clothing_budget,
            'utilities_budget': profile_model.utilities_budget,
            'transport_budget': profile_model.transport_budget,
            'others_budget': profile_model.others_budget,
        }

        return render(request, 'playground.html', context)

def delete_transactions(request, event_id):
    event = Transactions.objects.get(transaction_id=event_id)
    event.delete()
    return redirect('profile')

def delete_subscription(request, event_id):
    profile = request.user.username
    event = Subscriptions.objects.get(profile=profile, organization=event_id)
    event.delete()
    return redirect('profile')