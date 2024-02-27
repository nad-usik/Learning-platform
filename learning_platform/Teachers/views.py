from django.shortcuts import render, redirect
from Users.models import CustomUser
from .forms import AddForm
from .models import *
from django.db.models.functions import TruncDate
from django.utils import timezone
# from datetime import datetime


def teacher_dashboard(request):

    if request.user.is_authenticated:

        current_datetime = timezone.now()
        profile = CustomUser.objects.get(email=request.user.email)
        teacher = Teacher.objects.get(user_id=request.user)
        lessons = LessonSlot.objects.filter(teacher_id=teacher.id, date__date=current_datetime.date(), date__gte=current_datetime, is_available=False).order_by('date')

        if not lessons:
            any_available = False
        else:
            any_available = True
            registered_lessons = Lesson.objects.filter(lesson_id__in=lessons)
            student_profile = [(lesson.id, CustomUser.objects.get(id=Student.objects.get(id=lesson.student_id).user_id)) for lesson in registered_lessons]

        return render(request, 'teacher_dashboard.html', {'profile': profile, 'lessons': lessons, 'is_available': any_available, 'student_profile': student_profile})

    else:
        return redirect('login')


def teacher_calendar(request):
    # hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
    #          '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
    #          '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

    profile = CustomUser.objects.get(email=request.user.email)
    teacher = Teacher.objects.get(user_id=request.user)
    current_datetime = timezone.now()
    dates = LessonSlot.objects.filter(teacher_id=teacher.id, date__gte=current_datetime).annotate(date_only=TruncDate('date')).values('date_only').distinct().order_by('date_only').values_list('date_only', flat=True)
    lessons = LessonSlot.objects.filter(teacher_id=teacher.id, date__gte=current_datetime).order_by('date')

    context = {'call': 'calendar', 'profile': profile, 'lessons': lessons, 'dates': dates}

    return render(request, 'teacher_dashboard.html', context)


def add_lesson(request):
    form = AddForm(request.user.id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddForm(request.user.id, request.POST)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.teacher_id = Teacher.objects.get(user_id=request.user).id
                form.save()
                return redirect('teacher_calendar')
        else:
            return render(request, 'add_lesson.html', {'form': form})
    else:
        return render(request, 'home.html', {})
