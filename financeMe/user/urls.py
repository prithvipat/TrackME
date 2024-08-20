from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('transaction/', views.make_transaction, name='transactions'),
    path('profile/', views.check_transactions, name='profile')
]