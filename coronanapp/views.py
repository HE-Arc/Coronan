from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def profile(request):
    return render(request, 'profile.html', {})

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
    return render(request, 'login.html', {'form': form})

def add_bet(request):
    return render(request, 'add_bet.html', {})

def bets(request):
    return render(request, 'bets.html', {})

def insert_user(request):
    user = User.objects.create_user('Alexis', 'alexis.portmann@gmail.com', 'machintruc')
    user.profile.funds = 50
    user.save()
    return render(request, 'login.html', {})