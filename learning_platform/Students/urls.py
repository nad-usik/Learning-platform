from django.urls import path
from .views import *

urlpatterns = [
    path('', student_dashboard, name='student_dashboard'),
    path('calendar/', student_calendar, name='student_calendar'),
    # path('day/', my_day, name='my_day'),
    path('schedule/', schedule, name='schedule'),
    path('register_for_class/<int:pk>', register_for_class, name='register-for-class'),
]
