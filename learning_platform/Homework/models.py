from django.db import models
from django.contrib.postgres.fields import ArrayField
from Teachers.models import Teacher, Subjects
from Students.models import Student

class Assignment(models.Model):

    created = models.DateTimeField()
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)
    content = models.CharField()
    attached_file = models.FileField(upload_to='files/assignment_files/', blank=True, null=True)
    attached_image = models.ImageField(upload_to='images/assignment_images/', blank=True, null=True)
    checked = models.BooleanField(default=False)
    handed = models.BooleanField(default=False)
    response_content = models.CharField(null = True, blank=True)
    response_file = models.FileField(upload_to='files/response_files/', blank=True, null=True)

    def hand_task(self):
        self.handed = True
        self.save()

    def check_task(self):
        self.checked = True
        self.save()