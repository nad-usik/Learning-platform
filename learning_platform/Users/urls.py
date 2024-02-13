from django.urls import path
from Users.views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('create_profile/', create_profile, name='create_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('profile/', view_profile, name='profile'),
]
