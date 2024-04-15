from django.db import models
from Users.models import CustomUser
from Teachers.models import Teacher
from Students.models import Student
from django.utils import timezone


class TeacherStudent(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    @classmethod
    def create_relation(cls, student, teacher):
        relation = cls(teacher=teacher, student=student)
        relation.save()
        return relation


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


