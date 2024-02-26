from django.urls import path
from Teachers.views import *

urlpatterns = [
    path('', teacher_dashboard, name='teacher_dashboard'),
    path('calendar/', teacher_calendar, name='teacher_calendar'),
    path('calendar/add', add_lesson, name='add_lesson'),
    # path('my_teachers/', student_teacher, name='my_teachers'),
    # path('my_day/', student_day, name='my_day')
]
