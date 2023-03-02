from django.contrib import admin
from django.urls import path, include
from tasks.views import sentEmail, tasks, users, taskuser

urlpatterns = [
    path('', sentEmail, name='email'),
    path('tasks', tasks, name='zadania'),
    path('users', users, name='uzytkownicy'),
    path('taskuser/<id>/', taskuser, name='taskuser'),
    path('admin/', admin.site.urls),
    path('task/', include('tasks.urls')),
]
