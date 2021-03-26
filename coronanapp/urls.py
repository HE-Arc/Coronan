from django.urls import path
from coronanapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('addFunds/', views.add_funds, name='add_funds'),
    path('signUp/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('addBet/', views.add_bet, name='add_bet'),
    path('bets/', views.bets, name='bets'),
    path('insert_user/', views.insert_user, name='insert_user'),
]