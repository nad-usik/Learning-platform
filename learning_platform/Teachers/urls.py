from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('calendar/', teacher_calendar, name='teacher_calendar'),
    path('calendar/<int:pk>', teacher_calendar, name='delete_lesson'),
    path('my-students/', show_students, name='teacher_students'),
]
