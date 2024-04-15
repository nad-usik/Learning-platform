from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='chat'),
    path('messages/<int:pk>', chat_view, name='chat_view'),
    path('sent_msg/<int:pk>', sent_messages, name='sent_msg'),
    path('receive_msg/<int:pk>', received_messages, name='receive_msg'),
    path('notification', chat_notification, name='notification')
]
