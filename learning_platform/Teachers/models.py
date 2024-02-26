from django.db import models
from Users.models import CustomUser
from Students.models import Student


class Subjects(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subjects)

    def __str__(self):
        return f'{self.user.email}, {self.user.role}, {self.subject}'


class LessonSlot(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.teacher} - {self.date}'

    def register_slot(self):
        self.is_available = False
        self.save()


# class Records(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     duration = models.DurationField()
#
#     def __str__(self):
#         return f'{self.teacher.user.email} - {self.student.user.email} ({self.date})'


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(LessonSlot, on_delete=models.CASCADE)
    record_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.user.email} - {self.lesson}'

    @classmethod
    def add(cls, student_id, lesson_slot):
        lesson = cls(student=student_id, lesson=lesson_slot)
        lesson.save()
        return lesson
