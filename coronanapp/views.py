from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile, Bet
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
    return render(request, 'add_funds.html', {})

def sign_up(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
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
    return render(request, 'add_bet.html', {})

def bets(request):
    user_bets = Bet.objects.all().filter(user=request.user)
    template = 'bets.html'
    bets = {
        'bets': user_bets
    }
    return render(request, template, bets)