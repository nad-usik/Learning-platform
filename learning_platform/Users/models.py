from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
import os
from django.conf import settings
from PIL import Image
# from django.db.models.signals import post_save


class CustomUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            password,
            role,
            last_name,
            first_name,
            second_name,
            date_of_birth,
            gender,
            town,
            phone_number,
            profile_photo,
            **extra_fields
    ):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)  # lowercase the domain
        user = self.model(
            email=email,
            role=role,
            last_name=last_name,
            first_name=first_name,
            second_name=second_name,
            date_of_birth=date_of_birth,
            gender=gender,
            town=town,
            phone_number=phone_number,
            profile_photo=profile_photo,
            **extra_fields
        )
        user.set_password(password)  # hash raw password and set
        user.save()
        return user

    def create_superuser(
            self,
            email,
            password,
            **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("date_of_birth", "2003-01-03")
        extra_fields.setdefault("role", 'teacher')
        extra_fields.setdefault("last_name", 'admin')
        extra_fields.setdefault("first_name", 'admin')
        extra_fields.setdefault("gender", 'female')
        extra_fields.setdefault("second_name", 'admin')
        extra_fields.setdefault("town", 'town')
        extra_fields.setdefault("phone_number", '')
        extra_fields.setdefault("profile_photo", None)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superuser must have is_staff=True.")
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must have is_superuser=True.")
            )
        return self.create_user(
            email,
            password,
            **extra_fields
        )


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    ROLE_CHOICES = [
        ('teacher', 'Преподаватель'),
        ('student', 'Ученик'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    GENDER_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    town = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to='images/profile_photo/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return f'{self.email}, {self.last_name} , {self.first_name}, {self.role}'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_photo:
            img = Image.open(self.profile_photo.path)

            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.profile_photo.path)

        elif self.first_name:
            folder_path = ('images/profile_photo/')
            if self.role == 'teacher' and self.gender == 'Женский':
                image_files = [f'teacher_woman_{i}.png' for i in range(1, 3)]
            elif self.role == 'teacher' and self.gender == 'Мужской':
                image_files = [f'teacher_man_{i}.png' for i in range(1, 3)]
            elif self.role == 'student' and self.gender == 'Женский':
                image_files = [f'student_girl_{i}.png' for i in range(1, 3)]
            elif self.role == 'student' and self.gender == 'Мужской':
                image_files = [f'student_boy_{i}.png' for i in range(1, 3)]
            default_photo = random.choice(image_files)
            photo = folder_path + default_photo
            self.profile_photo = photo
            self.save()