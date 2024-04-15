from django.urls import path
from .views import *

urlpatterns = [
    path('', teacher_dashboard, name='teacher_dashboard'),
    path('calendar/', teacher_calendar, name='teacher_calendar'),
    path('calendar/add', add_lesson, name='add_lesson'),
    # path('my_day/', student_day, name='my_day')
]
