from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from Users.models import CustomUser
from Teachers.models import Teachers, Lessons, Subjects, TeacherStudent
from Homework.models import Assignment
from .models import *
# from datetime import datetime
from django.utils import timezone
from django.contrib import messages
# from django.db.models.functions import TruncDate


@login_required
def student_dashboard(request):
    student = Students.objects.get(user=request.user)
    lessons = Lessons.objects.filter(student_id=student.id).values('id')
    profile = CustomUser.objects.get(email=request.user.email)
    current_datetime = timezone.now()
    today_lessons = Lessons.objects.filter(id__in=lessons, date__date=current_datetime)
    current_assignments = Assignment.objects.filter(student_id=student.id, handed=False, deadline__gte=current_datetime)

    if not today_lessons:
        plans = False
    else:
        plans = True
        
    context = {'action': 'dashboard', 'lessons': today_lessons, 'profile': profile, 'plans': plans, 'student': student, 'assignments': current_assignments}
    return render(request, 'student_dashboard.html', context)


def register_for_class(request, pk):
    lesson = get_object_or_404(Lessons, id=request.POST.get('lesson_id'))
    if Lessons.objects.filter(id=lesson.id, is_available=False).exists():
        messages.warning(request, 'Это занятие уже занято')
    else:
        student_id = Students.objects.get(user=request.user)
        if not TeacherStudent.objects.filter(student=student_id, teacher=lesson.teacher.id):
            TeacherStudent.create_relation(student_id, lesson.teacher)
        Lessons.book_lesson(lesson, student_id)
        messages.success(request, 'Вы успешно записались на зянятие')
    return HttpResponseRedirect(reverse('slots'))


@login_required
def student_calendar(request):

    profile = CustomUser.objects.get(email=request.user.email)
    student = Students.objects.get(user=request.user)
    lessons = Lessons.objects.filter(student_id=student.id).order_by('date')

    context = {'action': 'calendar', 'lessons': lessons, 'profile': profile, 'student': student}

    return render(request, 'student_calendar.html', context)


def slots(request):

    current_datetime = timezone.now()
    lessons = Lessons.objects.filter(is_available=True, date__gte=current_datetime).order_by(
        'date')
    
    if not lessons:
        available_classes = False
        context = {'available_classes': available_classes}
    else:
        available_classes = True
        context = {'lessons': lessons, 'available_classes': available_classes}

    return render(request, 'student_slots_list.html', context)


def search_subject(request):
    current_datetime = timezone.now()
    if request.method == 'POST':
        searched = request.POST['search']
        subject = Subjects.objects.get(name__contains=searched)
        lessons = Lessons.objects.filter(is_available=True, date__gte=current_datetime, subject_id=subject.id).order_by('date')
        if not lessons:
            available_classes = False
            context = {'available_classes': available_classes}
        else:
            available_classes = True
            context = {'lessons': lessons, 'available_classes': available_classes}
        return render(request, 'student_slots_list.html', context)
    else:
        return HttpResponseRedirect(reverse('slots'))


def show_teachers(request):

    user = request.user
    student = Students.objects.get(user_id=user)
    teachers_students = TeacherStudent.objects.filter(student_id=student).values_list('teacher_id', flat=True)
    teachers = Teachers.objects.filter(id__in=teachers_students)

    context = {'action': 'my_teachers', 'teachers': teachers, 'student': student}
    return render(request, 'student_teachers.html', context)