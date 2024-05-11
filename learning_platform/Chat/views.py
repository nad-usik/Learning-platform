from django.shortcuts import render, redirect
from .models import ChatMessages
from Users.models import CustomUser
from Students.models import Students
from Teachers.models import Teachers, TeacherStudent
from .forms import ChatMessageForm
from django.http import JsonResponse
import json
from django.core.serializers import serialize
from django.utils import timezone


def index(request):
    user = CustomUser.objects.get(email=request.user.email)
    if user.role == 'student':
        teachers = TeacherStudent.objects.filter(student_id=Students.objects.get(user_id=user.id)).values_list(
            'teacher', flat=True)
        connections = Teachers.objects.filter(id__in=teachers)

    else:
        students = TeacherStudent.objects.filter(teacher_id=Teachers.objects.get(user_id=user.id)).values_list(
            'student', flat=True)
        connections = Students.objects.filter(id__in=students)
    context = {'connections': connections,}

    return render(request, 'index.html', context)


def chat_view(request, pk):
    user = CustomUser.objects.get(email=request.user.email)
    profile = CustomUser.objects.get(id=pk)
    rec_chat = ChatMessages.objects.filter(sender=profile, receiver=user)
    rec_chat.update(seen=True)
    chats = ChatMessages.objects.all().order_by('time')
    form = ChatMessageForm()

    if user.role == 'student':
        teachers = TeacherStudent.objects.filter(student_id=Students.objects.get(user_id=user.id)).values_list(
            'teacher', flat=True)
        connections = Teachers.objects.filter(id__in=teachers)
        # current_receiver = Teachers.objects.get(user=pk)

    else:
        students = TeacherStudent.objects.filter(teacher_id=Teachers.objects.get(user_id=user.id)).values_list(
            'student', flat=True)
        connections = Students.objects.filter(id__in=students)
        # current_receiver = Students.objects.get(user=pk)

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = user
            msg.receiver = profile
            msg.save()
            return redirect("chat_view", pk=profile.id)

    context = {'connections': connections, 'profile': profile, 'user': user, 'form': form, 'chats': chats, 'num': rec_chat.count()}

    return render(request, 'chat.html', context)


def sent_messages(request, pk):
    user = request.user
    profile = CustomUser.objects.get(id=pk)
    data = json.loads(request.body)
    new_chat = data["msg"]
    chat_message = ChatMessages.create_message(new_chat, user, profile)
    serialized_data = serialize('json', [chat_message])

    return JsonResponse(serialized_data, safe=False)


def received_messages(request, pk):
    user = request.user
    profile = CustomUser.objects.get(id=pk)
    chat_message = ChatMessages.objects.filter(sender=profile, receiver=user)
    array = []
    for chat in chat_message:
        array.append([chat.body, chat.time])

    return JsonResponse(array, safe=False)

def chat_notification(request):
    user = request.user

    if user.role == 'student':
        teachers = TeacherStudent.objects.filter(student_id=Students.objects.get(user_id=user.id)).values_list(
            'teacher', flat=True)
        connections = Teachers.objects.filter(id__in=teachers).values_list("user_id", flat=True)
        # current_receiver = Teachers.objects.get(user=pk)

    else:
        students = TeacherStudent.objects.filter(teacher_id=Teachers.objects.get(user_id=user.id)).values_list(
            'student', flat=True)
        connections = Students.objects.filter(id__in=students).values_list("user_id", flat=True)
        # current_receiver = Students.objects.get(user=pk)

    array = []
    for item in connections:
        chats = ChatMessages.objects.filter(sender=item, receiver=user, seen=False)
        array.append(chats.count())
    
    return JsonResponse(array, safe=False)