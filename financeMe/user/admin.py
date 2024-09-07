from django.contrib import admin
from .models import Subscriptions, Transactions, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Transactions)
admin.site.register(Subscriptions)

