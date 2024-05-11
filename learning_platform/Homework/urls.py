from django.urls import path
from .views import *

urlpatterns = [
    path('', student_task_list, name='student_task_list'),
    path('current/<int:pk>', view_current_tasks, name='view_current_tasks'),
    path('finished/<int:pk>', view_finished_tasks, name='view_finished_tasks'),
    path('task_content/<int:pk>', view_content, name='view_content'),
    path('create_task/<int:pk>', create_task, name='create_task'),
    path('task_contnet/check/<int:pk>', check_task, name='check_task'),
    path('task_contnet/cancel/<int:pk>', cancel_response, name='cancel_response'),
]
