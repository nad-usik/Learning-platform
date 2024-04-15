from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
# from Users.models import CustomUser
from Teachers.models import Teacher
from Students.models import Student
from Chat.models import TeacherStudent
from .forms import AssignmentCreationForm, ResponseForm
from .models import *
# from django.db.models.functions import TruncDate
from django.utils import timezone
# from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import os

def create_task(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    
    form = AssignmentCreationForm(user)
    if request.method == 'POST':
        form = AssignmentCreationForm(user, request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher_id = Teacher.objects.get(user_id=user).id
            assignment.student_id = pk;
            assignment.created = timezone.now()
            if 'attached_file' in request.FILES:
                assignment.attached_file = request.FILES['attached_file']
            if 'attached_image' in request.FILES:    
                assignment.attached_image = request.FILES['attached_image']
                
            assignment.save()
            return redirect('view_current_tasks', pk=pk)
        else:
            form = AssignmentCreationForm(user)

    context = {'profile': user, 'form': form, 'student': student}
    
    return render(request, 'create_task.html', context)


def student_task_list(request):
    user = request.user
    students = Student.objects.filter(id__in=TeacherStudent.objects.filter(teacher=Teacher.objects.get(user_id=user)).values_list('student', flat=True))
    context = {'profile' : user, 'students': students}
    return render(request, 'student_task_list.html', context)


def view_current_tasks(request, pk): 
    user = request.user
    student = Student.objects.get(id=pk)
    current_date = timezone.now()
    
    if Teacher.objects.filter(user_id=user.id).exists():
        
        assignments = Assignment.objects.filter(student_id=student.id, teacher_id=Teacher.objects.get(user_id=user.id).id, deadline__gte=current_date).order_by('deadline')
        is_teacher = True
    
    elif Student.objects.filter(user_id=user.id).exists():
        assignments = Assignment.objects.filter(student_id=student.id, deadline__gte=current_date, handed=False).order_by('deadline')
        is_teacher = False

    context = {'profile': user, 'assignments': assignments, 'student': student, 'is_teacher': is_teacher}

    return render(request, 'current_tasks.html', context)


def view_finished_tasks(request, pk): 
    user = request.user
    student = Student.objects.get(id=pk)
    current_date = timezone.now()
    if Teacher.objects.filter(user_id=user.id).exists():
        
        assignments = Assignment.objects.filter(student_id=student.id, teacher_id=Teacher.objects.get(user_id=user.id).id, deadline__lt=current_date).order_by('deadline')
        is_teacher = True
    
    elif Student.objects.filter(user_id=user.id).exists():
        assignments = Assignment.objects.filter(Q(student_id=student.id, deadline__lt=current_date) | Q(handed=True)).order_by('deadline')
        is_teacher = False

    context = {'profile': user, 'assignments': assignments, 'student': student, 'is_teacher': is_teacher}
    return render(request, 'finished_tasks.html', context)


def view_content(request, pk):
    user = request.user
    assignment = Assignment.objects.get(id=pk)
    student = Student.objects.get(id = assignment.student.id)
    # file_name = os.path.basename(assignment.attached_file.name)
    # img_name = os.path.basename(assignment.attached_image.name)
    
    if Teacher.objects.filter(user_id=user.id).exists():
        is_teacher = True
    
    elif Student.objects.filter(user_id=user.id).exists():
        is_teacher = False
        
    form = ResponseForm(instance=assignment)
    if request.method == 'POST':
        form = ResponseForm( request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            ast = form.save(commit=False)
            ast.response_file = request.FILES['response_file']
            ast.hand_task()
            ast.save()
            return redirect('view_content', pk=pk)

    context = {'form': form, 'profile': user, 'assignment': assignment, 'student': student, 'is_teacher': is_teacher}
    return render(request, 'view_content.html', context)


def check_task(request, pk):
    assignment = get_object_or_404(Assignment, id=pk)
    assignment.check_task()
    return HttpResponseRedirect(reverse('view_content', args=[pk]))