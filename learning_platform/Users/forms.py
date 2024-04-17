from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from Teachers.models import Subjects, Teacher


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "role", "password", "last_name", "first_name", "second_name", "date_of_birth", "gender",
                  "town", "phone_number", "profile_photo", "is_staff",
                  "is_active",
                  ]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["email", "role", "password", "last_name", "first_name", "second_name", "date_of_birth", "gender",
                  "town", "phone_number", "profile_photo", "is_staff",
                  "is_active",
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
    last_name = forms.CharField(label='Фамилия', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}))
    first_name = forms.CharField(label='Имя', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}))
    second_name = forms.CharField(label='Отчество', max_length=50,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванович'}),
                                  required=False)
    date_of_birth = forms.DateField(label='Дата Рождения', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.CharField(label='Пол', widget=forms.Select(choices=CustomUser.GENDER_CHOICES,
                                                           attrs={'class': 'form-control', 'placeholder': 'Пол'}))
    town = forms.CharField(label='Город', widget=forms.TextInput(attrs={'placeholder': 'Москва', 'class': 'form-control'}))
    phone_number = forms.CharField(label='Номер Телефона', widget=forms.TextInput(
        attrs={'placeholder': '88001234567', 'class': 'form-control'}))
    profile_photo = forms.ImageField(label='Фото Профиля',
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01', 'placeholder': 'Dugfhdbuejh'}),
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
    subjects = forms.ModelMultipleChoiceField(label='', queryset=Subjects.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': "form-check-input"}))

    class Meta:
        model = Teacher
        fields = ('subjects',)
        
