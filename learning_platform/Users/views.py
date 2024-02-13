from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, EmailLoginForm, ProfileForm, EditProfileForm
from .models import CustomUser, Profile


# from django.contrib.auth import get_user_model
#
# User = get_user_model()


def login_user(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
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
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                email = request.POST['email']
                password = request.POST['password1']
                user = authenticate(request, email=email, password=password)
                messages.success(request, ("Вы успешно зарегестривались"))
                login(request, user)
                messages.success(request, ("Вы вошли в аккаунт"))
                return redirect('create_profile')
            else:
                messages.success(request, ("Ошибка! Попробуйте снова"))
                return redirect('register')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        return render(request, 'profile.html', {})


def create_profile(request):
    if request.user.is_authenticated:
        form = ProfileForm(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.last_name = request.POST['last_name']
                profile.first_name = request.POST['first_name']
                profile.second_name = request.POST['second_name']
                profile.date_of_birth = request.POST['date_of_birth']
                profile.gender = request.POST['gender']
                profile.town = request.POST['town']
                profile.phone_number = request.POST['phone_number']
                profile.profile_photo = request.FILES['profile_photo']
                profile.save()
                return redirect('profile')
            else:
                messages.success(request, ("Ошибка! Попробуйте снова"))
                return redirect('create_profile')
        else:
            return render(request, 'create_profile.html', {'form': form})
    else:
        return render(request, 'profile.html', {})


def edit_profile(request):
    if request.user.is_authenticated:
        form = EditProfileForm(instance=request.user.profile)
        if request.method == "POST":
            form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.last_name = form.cleaned_data['last_name']
                profile.first_name = form.cleaned_data['first_name']
                profile.second_name = form.cleaned_data['second_name']
                profile.date_of_birth = form.cleaned_data['date_of_birth']
                profile.gender = form.cleaned_data['gender']
                profile.town = form.cleaned_data['town']
                profile.phone_number = form.cleaned_data['phone_number']
                if 'profile_photo' in request.FILES:
                    profile.profile_photo = request.FILES['profile_photo']
                profile.save()
                return redirect('profile')
            else:
                messages.success(request, ("Ошибка! Попробуйте снова"))
                return redirect('edit_profile')
        else:
            return render(request, 'edit_profile.html', {'form': form})
    else:
        return redirect('login')


def view_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)
        return render(request, 'profile.html', {'profile': profile})
    else:
        form = ProfileForm()
        return render(request, 'create_profile.html', {'form': form})
