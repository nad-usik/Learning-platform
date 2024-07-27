from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test

from .forms import SignUpForm, EmailLoginForm, ProfileForm, SubjectChoiceForm, ChangePasswordForm
from .models import CustomUser
from Students.models import Students
from Students.views import student_dashboard
from Teachers.models import Teachers
from Teachers.views import teacher_dashboard


def is_authenticated(user):
    if user.is_authenticated:
        return False
    else:
        return True


def create_account(request):
    form = SignUpForm()
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                role = form.cleaned_data['role']
                password = form.cleaned_data['password1']
                user = authenticate(request, email=email, password=password)
                messages.success(request, ("Вы успешно зарегистрировались!"))
                login(request, user)

                if role == 'teacher':
                    Teachers.objects.create(user=user)
                elif role == 'student':
                    Students.objects.create(user=user)
                    
                return redirect(reverse('profile') + '?action=create')
            else:
                messages.error(request, ("Ошибка! Попробуйте снова"))
                return redirect('create_account')
        else:
            return render(request, 'create_account.html', {'form': form})
    else:
        return render(request, 'profile.html', {})


def create_profile(request):
    user = request.user
    profile_form = ProfileForm(instance=user)
    subject_form = None
    if request.user.role == 'teacher':
        teacher = Teachers.objects.get(user_id=user.id)
        subject_form = SubjectChoiceForm(request.POST, instance=teacher)
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.last_name = profile_form.cleaned_data['last_name']
            profile.first_name = profile_form.cleaned_data['first_name']
            profile.second_name = profile_form.cleaned_data['second_name']
            profile.date_of_birth = profile_form.cleaned_data['date_of_birth']
            profile.gender = profile_form.cleaned_data['gender']
            profile.town = profile_form.cleaned_data['town']
            profile.phone_number = profile_form.cleaned_data['phone_number']            
            if request.FILES:
                profile.profile_photo = request.FILES['profile_photo']
            profile.save()
            if user.role == 'teacher' and subject_form.is_valid():
                subjects = subject_form.cleaned_data['subjects']
                teacher = Teachers.objects.get(user=request.user)
                teacher.subject.set(subjects)
            messages.success(request, ("Ваши данные успешно сохранены!"))
            return redirect(reverse('profile'))
        else:
            messages.error(request, ("Ошибка! Попробуйте снова"))
            return redirect(reverse('profile') + '?action=create')
    else:
        return render(request, 'create_profile.html', {'profile_form': profile_form, 'subject_form': subject_form})     


def edit_profile(request):
    user = request.user
    profile_form = ProfileForm(instance=user)
    password_form = ChangePasswordForm()
    subject_form = None
    if user.role == 'teacher':
        teacher = Teachers.objects.get(user=user)
        subjects = teacher.subject.all()
        subject_form = SubjectChoiceForm(instance=teacher, initial={'subjects': subjects})
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=user)
        if user.role == 'teacher':
            subject_form = SubjectChoiceForm(request.POST, instance=teacher)
        password_form = ChangePasswordForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.last_name = profile_form.cleaned_data['last_name']
            profile.first_name = profile_form.cleaned_data['first_name']
            profile.second_name = profile_form.cleaned_data['second_name']
            profile.date_of_birth = profile_form.cleaned_data['date_of_birth']
            profile.gender = profile_form.cleaned_data['gender']
            profile.town = profile_form.cleaned_data['town']
            profile.phone_number = profile_form.cleaned_data['phone_number']
            if request.FILES:
                profile.profile_photo = request.FILES['profile_photo']
            profile.save()
            if user.role == 'teacher':
                if subject_form.is_valid():
                    subjects = subject_form.cleaned_data['subjects']
                    teacher = Teachers.objects.get(user=user)
                    teacher.subject.clear()
                    teacher.subject.set(subjects)
                else:
                    messages.error(request, ("Ошибка при выборе предмета! Попробуйте снова"))
                    return redirect(reverse('profile') + '?action=edit')
            if password_form.is_valid():
                old_password = password_form.cleaned_data.get('old_password')
                new_password = password_form.cleaned_data.get('new_password')
                if old_password:
                    if user.check_password(old_password):
                        user.set_password(new_password)
                        user.save()
                        messages.success(request, "Пароль успешно изменён")
                        login(request, user)
                    else:
                        messages.error(request, ("Не верный пароль! Попробуйте снова"))
            messages.success(request, ("Изменения успешно сохранены!"))
            return redirect('profile')
        else:
            messages.error(request, ("Ошибка! Попробуйте снова"))
            return redirect(reverse('profile') + '?action=edit')
    else:
        return render(request, 'edit_profile.html', {'profile_form': profile_form, 'subject_form': subject_form, 'password_form': password_form})


def delete_account(request):
    user = request.user
    account = CustomUser.objects.get(id=user.id)
    account.delete()
    messages.success(request, ("Ваш аккаунт успешно удалён!"))
    return redirect('/')


def profile(request):
    user = request.user

    if user.is_authenticated:
        action = request.GET.get('action')
        if action == 'create':
            return create_profile(request)
        elif action == 'edit':
            return edit_profile(request)
        elif action == 'delete':
            return delete_account(request)
        else:
            profile = CustomUser.objects.get(email=request.user.email)
            return render(request, 'profile.html', {'profile': profile})
    else:
        return render(request, 'login.html', {})


@user_passes_test(is_authenticated)
def login_user(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("Вы успешно вошли в аккаунт!"))
                if user.role == 'student':
                    return student_dashboard(request)
                elif user.role == 'teacher':
                    profile = CustomUser.objects.get(email=request.user.email)
                    return teacher_dashboard(request)
                else:
                    return redirect('home')
            else:
                messages.error(request, ("Ошибка! Неверная почта или пароль"))
                return redirect('login')
        else:
            messages.error(request, ("Ошибка! Повторите попытку"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Вы вышли из аккаунта"))
    return redirect('login')