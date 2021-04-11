from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile, Bet
from .forms import BetForm, FundsForm
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile
    }
    template = 'profile.html'  
    return render(request, template, context)

def add_funds(request):
    if request.method == 'POST':
        form = FundsForm(request.POST)
        if form.is_valid():
            funds = form.cleaned_data.get('funds')
            profile = Profile.objects.get(user=request.user)
            profile.funds += funds
            profile.save()
            return redirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FundsForm()
    return render(request, 'add_funds.html', {'form': form})

def sign_up(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        profile = Profile.objects.get(user=request.user)
        profile.funds = 0
        profile.save()
        return redirect('home')
    return render(request, 'sign_up.html', {'form': form})

def login_user(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password.")
    else:
        messages.error(request,"Invalid username or password.")
    return render(request, 'login.html', context={'form': form})

def add_bet(request):
    if request.method == 'POST':
        form = BetForm(request.POST)

        if form.is_valid():
            cases = form.cleaned_data.get('cases')
            sum = form.cleaned_data.get('sum')
            bet = Bet(moneyBet=sum, cases=cases, user=request.user)
            bet.save()
            return redirect('/bets/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BetForm()
    return render(request, 'add_bet.html', {'form': form})

def bets(request):
    user_bets = Bet.objects.all().filter(user=request.user)
    template = 'bets.html'
    bets = {
        'bets': user_bets
    }
    return render(request, template, bets)