from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


# from django.db.models.signals import post_save

# Registrate a user
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=False, null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=150)
    ROLE_CHOICES = [
        ('teacher', 'Преподаватель'),
        ('student', 'Ученик'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}, {self.role}'


# Fill in user's profile
class Profile(models.Model):
    # profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('Male', 'Мужской'),
        ('Female', 'Женский'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    town = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to='images/profile_photo/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_photo:
            img = Image.open(self.profile_photo.path)

            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.profile_photo.path)

    def __str__(self):
        return f'{self.last_name} , {self.first_name}'

