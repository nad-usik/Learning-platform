from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, EmailLoginForm
from django import forms


def login_user(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = request.POST['password']
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("Вы вошли в аккаунт"))
                return redirect('/')
            else:
                messages.success(request, ("Ошибка! Повторите попытку"))
                return redirect('login')
        else:
            messages.success(request, ("Ошибка! Повторите попытку"))
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Вы вышли из аккаунта"))
    return redirect('/')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            messages.success(request, ("Вы успешно зарегестривались"))
            login(request, user)
            messages.success(request, ("Вы вошли в аккаунт"))
            return redirect('/')
        else:
            messages.success(request, ("Ошибка! Попробуйте снова"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
