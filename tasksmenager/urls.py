from django.contrib import admin
from django.urls import path, include
from tasks.views import *

urlpatterns = [
    path('', loginPage, name='login'),
    path('tasks', tasks, name='zadania'),
    path('users', users, name='uzytkownicy'),
    path('taskuser/<id>/', taskuser, name='taskuser'),
    path('admin/', admin.site.urls),
    path('task/', include('tasks.urls')),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name='logout'),
    path('taskdetails/<id>', taskdetails, name='szczegoly'),
]
