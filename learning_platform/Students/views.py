from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from Users.models import CustomUser
from Teachers.models import Teacher, Lesson
from Chat.models import TeacherStudent
from .models import *
# from datetime import datetime
from django.utils import timezone
from django.contrib import messages
# from django.db.models.functions import TruncDate


@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    lessons = Lesson.objects.filter(student_id=student.id).values('id')
    profile = CustomUser.objects.get(email=request.user.email)
    current_datetime = timezone.now()
    today_lessons = Lesson.objects.filter(id__in=lessons, date__date=current_datetime)

    if not today_lessons:
        plans = False
    else:
        plans = True
        
    context = {'call': 'my_day', 'lessons': today_lessons, 'profile': profile, 'plans': plans, 'student': student}
    return render(request, 'student_dashboard.html', context)


def register_for_class(request, pk):
    lesson = get_object_or_404(Lesson, id=request.POST.get('lesson_id'))
    if Lesson.objects.filter(id=lesson.id, is_available=False).exists():
        messages.warning(request, 'You are already registered for this class.')
    else:
        student_id = Student.objects.get(user=request.user)
        if not TeacherStudent.objects.filter(student=student_id, teacher=lesson.teacher.id):
            TeacherStudent.create_relation(student_id, lesson.teacher)
        Lesson.book_lesson(lesson, student_id)
        messages.success(request, 'Successfully registered for the class.')
    return HttpResponseRedirect(reverse('schedule'))


@login_required
def student_calendar(request):

    profile = CustomUser.objects.get(email=request.user.email)
    student = Student.objects.get(user=request.user)
    lessons = Lesson.objects.filter(student_id=student.id).order_by('date')

    context = {'call': 'calendar', 'lessons': lessons, 'profile': profile, 'student': student}

    return render(request, 'student_dashboard.html', context)


def schedule(request):

    current_datetime = timezone.now()
    # available_teachers = Lesson.objects.filter(is_available=True,
    #                                            date__gte=current_datetime).distinct().values_list('teacher',
    #                                                                                               flat=True).order_by(
    #     'teacher')
    lessons = Lesson.objects.filter(is_available=True, date__gte=current_datetime).order_by(
        'date')
    # dates = Lesson.objects.filter(is_available=True, date__gte=current_datetime).annotate(
    #     date_only=TruncDate('date')).values('date_only').distinct().order_by('date_only').values_list('date_only',
    #                                                                                                   flat=True)

    if not lessons:
        available_classes = False
        context = {'available_classes': available_classes}
    else:
        # profile = [(available_teacher, CustomUser.objects.get(id=Teacher.objects.get(id=available_teacher).user_id)) for
        #            available_teacher in available_teachers]
        available_classes = True
        context = {'lessons': lessons, 'available_classes': available_classes}

    return render(request, 'student_schedule.html', context)