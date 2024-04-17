from django.urls import path
from Users.views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', register_user, name='register'),
    path('profile/', profile, name='profile'),
]
