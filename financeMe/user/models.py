from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()
CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Transportation', 'Transportation'),
    ('Clothing', 'Clothing'),
    ('Utilities', 'Utilities'),
    ('Vacation', 'Vacation'),
    ('Others', 'Others')
]

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    balance = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Transactions(models.Model):
    profile = models.CharField(max_length=100)
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(blank=False)
    transaction_type = models.BooleanField() # True = Transaction in False = Transaction out
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True) # If blank must be money made
    retailer = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # notes = models.TextField(max_length=100, blank=True)

#class Income(models.Model):
    #profile = models.CharField(max_length=100)
    #income = models.DecimalField(max_digits=12, decimal_places=2)
    #mainIncome = models.BooleanField() True for Main Income

"""
class Subscriptions(models.Model):
    profile = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Monthly Price
"""