from django.db import models
from Users.models import CustomUser
from django.utils import timezone



class ChatMessages(models.Model):
    body = models.TextField()
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    time = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)
    
    @classmethod
    def create_message(cls, msg_body, msg_sender, msg_receiver):
        message = cls(body=msg_body, sender=msg_sender, receiver=msg_receiver, time=timezone.now())
        message.save()
        return message


