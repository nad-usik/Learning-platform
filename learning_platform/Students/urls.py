from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('calendar/', student_calendar, name='student_calendar'),
    path('slots/', slots, name='slots'),
    path('register-for-class/<int:pk>', register_for_class, name='register-for-class'),
    # path('slots/search', search_subject, name='search_subject'),
    path('my-teachers', show_teachers, name='student_teachers'),
    path('my_teachers/profile/<int:pk>', view_profile, name='view_teacher_profile')
]
