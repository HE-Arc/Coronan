from django.urls import path
from coronanapp import views
from .tasks import hourly_fetch

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('addFunds/', views.add_funds, name='add_funds'),
    path('signUp/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('addBet/', views.add_bet, name='add_bet'),
    path('bets/', views.bets, name='bets'),
    path('logout/', views.logout_user, name='logout'),
]

hourly_fetch(repeat=5, repeat_until=None)