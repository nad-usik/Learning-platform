from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from Users.models import Profile
from Teachers.models import Teacher, LessonSlot, Lesson
from .models import *
# from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.db.models.functions import TruncDate


@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    lessons = Lesson.objects.filter(student_id=student.id).values('lesson_id')
    profile = Profile.objects.get(user=request.user)
    current_datetime = timezone.now()
    today_lessons = LessonSlot.objects.filter(id__in=lessons, date__date=current_datetime)

    context = {'call': 'my_day', 'lessons': today_lessons, 'profile': profile}
    return render(request, 'student_dashboard.html', context)


def register_for_class(request, pk):
    lesson = get_object_or_404(LessonSlot, id=request.POST.get('lesson_id'))

    if Lesson.objects.filter(lesson_id=lesson.id).exists():
        messages.warning(request, 'You are already registered for this class.')
    else:
        student_id = Student.objects.get(user=request.user)
        Lesson.add(student_id, lesson)
        LessonSlot.register_slot(lesson)
        messages.success(request, 'Successfully registered for the class.')
    return HttpResponseRedirect(reverse('schedule'))


@login_required
def student_calendar(request):
    # hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
    #          '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
    #          '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    current_datetime = timezone.now()

    student = Student.objects.get(user=request.user)
    lessons = Lesson.objects.filter(student_id=student.id).values('lesson_id')
    profile = Profile.objects.get(user=request.user)
    dates = LessonSlot.objects.filter(id__in=lessons, date__gte=current_datetime).annotate(
        date_only=TruncDate('date')).values('date_only').distinct().order_by('date_only').values_list('date_only',
                                                                                                      flat=True)
    current_lessons = LessonSlot.objects.filter(id__in=lessons, date__gte=current_datetime).order_by('date')
    teacher_ids = current_lessons.values_list('teacher_id', flat=True)
    teachers = Teacher.objects.filter(id__in=teacher_ids).values_list('user', flat=True).values('id', 'user')

    context = {'call': 'calendar', 'lessons': current_lessons, 'dates': dates, 'teachers': teachers, 'profile': profile}

    return render(request, 'student_dashboard.html', context)


# def student_teacher(request):
#     profile = Profile.objects.get(user=request.user)
#     teachers = TeacherForStudent.objects.filter(student=request.user)
#     teachers_profiles = [t.teacher.profile for t in teachers]
#     # for i in teachers:
#     #     print(i.teacher_id.profile.last_name)
#     context = {'call': 'my_teachers', 'teachers': teachers_profiles}
#     return render(request, 'student_dashboard.html', context)


# def student_dashboard(request):
#     if request.user.is_authenticated:
#         profile = Profile.objects.get(user=request.user)
#         return render(request, 'student_dashboard.html', {'profile': profile})
#     else:
#         return redirect('login')


def schedule(request):
    current_datetime = timezone.now()
    available_teachers = LessonSlot.objects.filter(is_available=True,
                                                   date__gte=current_datetime).distinct().values_list('teacher',
                                                                                                      flat=True).order_by(
        'teacher')
    lessons = LessonSlot.objects.filter(is_available=True, date__gte=current_datetime).order_by(
            'date')
    # dates = LessonSlot.objects.filter(is_available=True, date__gte=current_datetime).annotate(
    #     date_only=TruncDate('date')).values('date_only').distinct().order_by('date_only').values_list('date_only',
    #                                                                                                   flat=True)

    if not lessons:
        available_classes = False
        context = {'available_classes': available_classes}
    else:
        profile = [(available_teacher, Profile.objects.get(user=Teacher.objects.get(id=available_teacher).user)) for
                   available_teacher in available_teachers]

        print(lessons)
        available_classes = True
        context = {'lessons': lessons, 'profile': profile, 'teachers': available_teachers,
                   'available_classes': available_classes}

    return render(request, 'student_schedule.html', context)

# def student_day(request):
#     profile = Profile.objects.get(user=request.user)
#     context = {'call': 'my_day', 'profile': profile}
#     return render(request, 'student_dashboard.html', context)
