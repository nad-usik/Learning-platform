from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

from Teachers.models import Subjects, Teacher


# from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "role", "password", "last_name", "first_name", "second_name", "date_of_birth", "gender",
                  "town", "phone_number", "profile_photo", "is_staff",
                  "is_active",
                  # "groups",
                  # "user_permissions"
                  ]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["email", "role", "password", "last_name", "first_name", "second_name", "date_of_birth", "gender",
                  "town", "phone_number", "profile_photo", "is_staff",
                  "is_active",
                  # "groups",
                  # "user_permissions"
                  ]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}))
    role = forms.CharField(label='', widget=forms.Select(choices=CustomUser.ROLE_CHOICES,
                                                         attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label="",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'role', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    last_name = forms.CharField(label='', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(label='', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    second_name = forms.CharField(label='', max_length=50,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
                                  required=False)
    date_of_birth = forms.DateField(label='', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.CharField(label='', widget=forms.Select(choices=CustomUser.GENDER_CHOICES,
                                                           attrs={'class': 'form-control', 'placeholder': 'Пол'}))
    town = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Город', 'class': 'form-control'}))
    phone_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Номер Телефона', 'class': 'form-control'}))
    profile_photo = forms.ImageField(label='',
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01'}),
                                     required=False)

    class Meta:
        model = CustomUser
        fields = (
            'last_name', 'first_name', 'second_name', 'date_of_birth', 'gender', 'town', 'phone_number',
            'profile_photo')


class EditProfileForm(forms.ModelForm):
    last_name = forms.CharField(label='', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(label='', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    second_name = forms.CharField(label='', max_length=50,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
                                  required=False)
    date_of_birth = forms.DateField(label='', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.CharField(label='', widget=forms.Select(choices=CustomUser.GENDER_CHOICES,
                                                           attrs={'class': 'form-control', 'placeholder': 'Пол'}))
    town = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Город', 'class': 'form-control'}))
    phone_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Номер Телефона', 'class': 'form-control'}))
    profile_photo = forms.ImageField(label='',
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01'}),
                                     required=False)

    class Meta:
        model = CustomUser
        fields = (
            'last_name', 'first_name', 'second_name', 'date_of_birth', 'gender', 'town', 'phone_number',
            'profile_photo')


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Электронную Почту'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите Пароль', 'cols': '12'}))


class SubjectChoiceForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(), widget=forms.CheckboxSelectMultiple,
                                              label='Выберите предметы')

    class Meta:
        model = Teacher
        fields = ('subjects',)
