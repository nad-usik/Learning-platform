from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Registrate a user
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    ROLE_CHOICES = [
        ('teacher', 'Преподаватель'),
        ('student', 'Ученик'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


# Fill in user's profile
class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('Male', 'Мужской'),
        ('Female', 'Женский'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    town = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to='uploads/profile_photo/', blank=True, null=True)

    def __str__(self):
        return f'{self.surname} , {self.name}'


# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		user_profile = Profile(user=instance)
# 		user_profile.save()
#
# post_save.connect(create_profile, sender=User)
