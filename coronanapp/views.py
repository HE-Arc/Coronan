from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def add_funds(request):
    return render(request, 'add_funds.html', {})

def sign_up(request):
    return render(request, 'sign_up.html', {})

def login(request):
    return render(request, 'login.html', {})

def add_bet(request):
    return render(request, 'add_bet.html', {})

def bets(request):
    return render(request, 'bets.html', {})