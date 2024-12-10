from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import date, datetime


User = get_user_model()
CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Transportation', 'Transportation'),
    ('Clothing', 'Clothing'),
    ('Utilities', 'Utilities'),
    ('Groceries', 'Groceries'),
    ('Others', 'Others'),
    ('Income', 'Income')
]

INCOME_EXPENSE = [
    ('Expense', 'Expense'),
    ('Income', 'Income')
]

PAYMENT = [
    ('Weekly', 'Weekly'),
    ('Bi-Weekly', 'Bi-Weekly')
]

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    balance = models.DecimalField(blank=True, default=0, decimal_places=2, max_digits=10)
    food_budget = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=0)
    transport_budget = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=0)
    clothing_budget = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=0)
    utilities_budget = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=0)
    others_budget = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Transactions(models.Model):
    profile = models.CharField(max_length=100)
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(default=date.today())
    time = models.DateTimeField(default=datetime.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    retailer = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=INCOME_EXPENSE)
    # notes = models.TextField(max_length=100, blank=True)

class Subscriptions(models.Model):
    profile = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Monthly Price

    
class CSVFiles(models.Model):
    profile = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    year = models.IntegerField(default=int(date.today().year))
