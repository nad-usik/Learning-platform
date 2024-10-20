from django.urls import path
from Users.views import *

urlpatterns = [
    path('create-account/', create_account, name='create_account'),
    path('profile/', profile, name='profile'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
