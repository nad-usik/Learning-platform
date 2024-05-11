from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('users/', include('Users.urls')),
    path('student/', include('Students.urls')),
    path('teacher/', include('Teachers.urls')),
    path('chat/', include('Chat.urls')),
    path('tasks/', include('Homework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
