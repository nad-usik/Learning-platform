from django.db import models
from Users.models import CustomUser
from Students.models import Student
from django.utils import timezone


class Subjects(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subjects)

    def __str__(self):
        return f'{self.id}, {self.user.email}'


class Lesson(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.IntegerField()
    is_available = models.BooleanField(default=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    record_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.teacher} - {self.date}'

    def book_lesson(self, student):
        if self.is_available:
            self.is_available = False
            self.student = student
            self.record_time = timezone.now()
            self.save()
            return True
        return False

