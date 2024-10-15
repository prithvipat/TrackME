from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.check_transactions, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('delete_transactions/<event_id>',views.delete_transactions, name='delete_transactions'),
    path('delete_subscriptions/<event_id>', views.delete_subscriptions, name='delete_subscriptions'),
    path('delete/', views.delete_profile, name='delete'),
    path('playground/', views.playground, name='playground'),
    path('news/', views.news, name='news'),
    path('tips/', views.tips, name='tips'),
]