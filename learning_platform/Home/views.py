from django.shortcuts import render, redirect
# from Users.models import Profile

def home(request):
    return render(request, 'home.html', {})


