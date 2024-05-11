from django.db import models
from Users.models import CustomUser
from Students.models import Students
from django.utils import timezone


class Subjects(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Teachers(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subjects)

    def __str__(self):
        return f'{self.id}, {self.user.email}'

    @classmethod
    def delete(cls, pk):
        try:
            cls.objects.filter(user=pk).delete()
            return True
        except Exception as e:
            print("Ошибка при удалении записей:", e)
            return False


class TeacherStudent(models.Model):
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)

    @classmethod
    def create_relation(cls, student, teacher):
        relation = cls(teacher=teacher, student=student)
        relation.save()
        return relation


class Lessons(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.IntegerField()
    is_available = models.BooleanField(default=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id}, {self.date}'

    def book_lesson(self, student):
        if self.is_available:
            self.is_available = False
            self.student = student
            self.record_time = timezone.now()
            self.save()
            return True
        return False
    
    def delete_lesson(self):
        self.delete() 