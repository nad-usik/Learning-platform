from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignUpForm, EmailLoginForm, ProfileForm, EditProfileForm, SubjectChoiceForm
from .models import CustomUser
from Students.models import Student
from Teachers.models import Teacher, Subjects


def is_authenticated(user):
    if user.is_authenticated:
        return False
    else:
        return True


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
                messages.success(request, ("Вы вошли в аккаунт"))
                if user.role == 'student':
                    student = Student.objects.get(user_id=user)
                    profile = CustomUser.objects.get(email=request.user.email)
                    return render(request, 'student_dashboard.html', {'profile': profile, 'student': student})
                elif user.role == 'teacher':
                    profile = CustomUser.objects.get(email=request.user.email)
                    return render(request, 'teacher_dashboard.html', {'profile': profile})
                else:
                    return redirect('home')
            else:
                messages.error(request, ("Ошибка! Повторите попытку"))
                return redirect('login')
        else:
            messages.error(request, ("Ошибка! Повторите попытку"))
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
                email = form.cleaned_data['email']
                role = form.cleaned_data['role']
                password = form.cleaned_data['password1']
                user = authenticate(request, email=email, password=password)
                messages.success(request, ("Вы успешно зарегестривались"))
                login(request, user)
                # messages.success(request, ("Вы вошли в аккаунт"))

                if role == 'teacher':
                    Teacher.objects.create(user=user)
                elif role == 'student':
                    Student.objects.create(user=user)

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
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        subject_form = None
        if request.user.role == 'teacher':
            subject_form = SubjectChoiceForm(request.POST, instance=request.user)
        if request.method == "POST":

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

                if request.user.role == 'teacher' and subject_form.is_valid():
                    subjects = subject_form.cleaned_data['subjects']
                    teacher = Teacher.objects.get(user=request.user)
                    teacher.subject.set(subjects)

                return redirect('profile')
            else:
                messages.success(request, ("Ошибка! Попробуйте снова"))
                return redirect('create_profile')
        else:
            return render(request, 'create_profile.html', {'profile_form': profile_form, 'subject_form': subject_form})
    else:
        return render(request, 'profile.html', {})


def edit_profile(request):
    if request.user.is_authenticated:
        form = EditProfileForm(instance=request.user)
        if request.method == "POST":
            form = EditProfileForm(request.POST, request.FILES, instance=request.user)
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
                messages.error(request, ("Ошибка! Попробуйте снова"))
                return redirect('edit_profile')
        else:
            return render(request, 'edit_profile.html', {'form': form})
    else:
        return redirect('login')


def view_profile(request):
    if CustomUser.objects.filter(email=request.user.email).exists():
        profile = CustomUser.objects.get(email=request.user.email)
        return render(request, 'profile.html', {'profile': profile})
    else:
        form = ProfileForm()
        return render(request, 'create_profile.html', {'form': form})
