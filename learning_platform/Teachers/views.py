from django.shortcuts import render, redirect, get_object_or_404
from Users.models import CustomUser
from Students.models import Students
from Homework.models import Assignment
from .forms import AddLessonForm
from .models import *
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.http import JsonResponse

def teacher_dashboard(request):

    if request.user.is_authenticated:

        current_datetime = timezone.now()
        profile = CustomUser.objects.get(email=request.user.email)
        teacher = Teachers.objects.get(user_id=request.user)
        lessons = Lessons.objects.filter(teacher_id=teacher.id, date__date=current_datetime.date(), date__gte=current_datetime, is_available=False).order_by('date')
        assignments = Assignment.objects.filter(teacher_id=teacher, handed=True, checked=False)

        if not lessons:
            any_available = False
        else:
            any_available = True
           
        return render(request, 'teacher_dashboard.html', {'action': 'dashboard','profile': profile, 'lessons': lessons, 'is_available': any_available, 'assignments': assignments})

    else:
        return redirect('login')


def teacher_calendar(request, pk=None):

    user = request.user
    action = request.GET.get('action')

    if action =='add':
        return add_lesson(request)
    elif action == 'delete':
        return delete_lesson(request, pk)
    else :
        profile = CustomUser.objects.get(email=user.email)
        teacher = Teachers.objects.get(user_id=user)
        current_datetime = timezone.now()
        unavailable_lessons = Lessons.objects.filter(teacher_id=teacher.id, is_available=False, date__gte=current_datetime).order_by('date')
        all_lessons = Lessons.objects.filter(teacher_id=teacher.id, is_available=True, date__gte=current_datetime).order_by('date')
        
        context = {'action': 'calendar', 'profile': profile, 'unavailable_lessons': unavailable_lessons, 'all_lessons': all_lessons}
        return render(request, 'teacher_calendar.html', context)


def add_lesson(request):
    form = AddLessonForm(request.user.id)
    profile = CustomUser.objects.get(id=request.user.id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddLessonForm(request.user.id, request.POST)
            if form.is_valid():
                print("here")
                lesson = form.save(commit=False)
                lesson.teacher_id = Teachers.objects.get(user_id=request.user).id
                form.save()
                return redirect('teacher_calendar')
        else:
            return render(request, 'add_lesson.html', {'action': 'calendar', 'form': form, 'profile': profile})
    else:
        return render(request, 'home.html', {})
    

def delete_lesson(request, pk):
    lesson = get_object_or_404(Lessons, id=pk)
    if request.method == 'POST':
        lesson.delete_lesson()
    return redirect(teacher_calendar)


def show_students(request):
    user = request.user
    profile = CustomUser.objects.get(id=user.id)
    teacher = Teachers.objects.get(user_id=user)
    students_teachers = TeacherStudent.objects.filter(teacher_id=teacher).values_list('student_id', flat=True)
    students = Students.objects.filter(id__in=students_teachers)

    context = {'action': 'my_students', 'students': students, 'profile': profile}
    return render(request, 'teacher_students.html', context)