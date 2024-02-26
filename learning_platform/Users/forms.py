from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Profile
from Teachers.models import Subjects, Teacher

# from django.core.exceptions import ValidationError


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

    # def __init__(self, *args, **kwargs):
    #     super(SignUpForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    #     self.fields['password1'].label = ''
    #     self.fields[
    #         'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
    #
    #     self.fields['password2'].widget.attrs['class'] = 'form-control'
    #     self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
    #     self.fields['password2'].label = ''
    #     self.fields[
    #         'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class ProfileForm(forms.ModelForm):
    last_name = forms.CharField(label='', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(label='', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    second_name = forms.CharField(label='', max_length=50,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
                                  required=False)
    date_of_birth = forms.DateField(label='', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.CharField(label='', widget=forms.Select(choices=Profile.GENDER_CHOICES,
                                                           attrs={'class': 'form-control', 'placeholder': 'Пол'}))
    town = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Город', 'class': 'form-control'}))
    phone_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Номер Телефона', 'class': 'form-control'}))
    profile_photo = forms.ImageField(label='',
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01'}),
                                     required=False)

    class Meta:
        model = Profile
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
    gender = forms.CharField(label='', widget=forms.Select(choices=Profile.GENDER_CHOICES,
                                                           attrs={'class': 'form-control', 'placeholder': 'Пол'}))
    town = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Город', 'class': 'form-control'}))
    phone_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Номер Телефона', 'class': 'form-control'}))
    profile_photo = forms.ImageField(label='',
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'inputGroupFile01'}),
                                     required=False)

    class Meta:
        model = Profile
        fields = (
            'last_name', 'first_name', 'second_name', 'date_of_birth', 'gender', 'town', 'phone_number',
            'profile_photo')


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Электронную Почту'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите Пароль', 'cols': '12'}))


class SubjectChoiceForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(), widget=forms.CheckboxSelectMultiple, label='Выберите предметы')

    class Meta:
        model = Teacher
        fields = ('subjects', )
