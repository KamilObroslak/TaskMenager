from imaplib import _Authenticator
from django.contrib import messages
from django.shortcuts import redirect, render
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import *
import smtplib
import ssl  # import 2 modułów smtplib i ssl potrzebnych do wysyłki maila
from rest_framework import viewsets
from .serializer import TaskSerializer
from django.contrib.auth.models import User
from .models import Task
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


def sentEmail(request):

    now = datetime.today()
    y = datetime.date(now)

    tasks = Task.objects.all()

    for i in tasks:

        if i.expiry_date < y and i.status == "unresolved":

            port = 465  # port używany przez protokół ssl
            smtp_serwer = "smtp.gmail.com"
            sender = "kamilobroslak1@gmail.com"
            recipient = "kamilobroslak2@gmail.com"  # mail do testów formy maila i czy maile wychodza
            password = "xdaeyqlxwbxlqbca"  # przy wpisaniu hasła do konta google maile wychodzą i nie pojawia się błąd
            subject = "Masz niedokonczone zadania"
            content = """<h1>Masz niedokonczone zadania</h1>
                        <b>Sprawdz zadania przypisane do Ciebie. Zadanie: </b>""" + i.title + """
                        </b> W załączniku plik"""

            plik = "plik.txt"

            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = recipient
            message["Subject"] = subject

            message.attach(MIMEText(content, "html"))

            with open(plik, "rb") as f:
                attachment = MIMEBase("application", "octet-stream")
                attachment.set_payload(f.read())

            encoders.encode_base64(attachment)

            attachment.add_header(
                "Content-Disposition",
                f"attachment; filename= {plik}"
            )

            message.attach(attachment)
            text = message.as_string()

            ssl_pol = ssl.create_default_context()

            with smtplib.SMTP_SSL(smtp_serwer, port, context=ssl_pol) as serwer:
                serwer.login(sender, password)
                serwer.sendmail(sender, recipient, text)

            return render(request, 'template.html')


#  wymagany -> from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def tasks(request):
    tasks = Task.objects.all()
    data = {'zadania': tasks}
    sentEmail(request)
    return render(request, 'tasks.html', data)


@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    data = {'uzytkownicy': users}
    return render(request, 'users.html', data)


@login_required(login_url='login')
def taskuser(request, id):
    user_tasks = User.objects.get(pk=id)
    user_task = Task.objects.filter(user_id=user_tasks)
    data = {'wybor_uzytkownika': user_tasks,
            'zadania_uzytkownika': user_task}
    return render(request, 'taskuser.html', data)


@login_required(login_url='login')
def taskdetails(request, id):
    task_details = Task.objects.get(pk=id)
    task_detail = Task.objects.get(id=task_details.pk)
    data = {'wybor_uzytkownika': task_details,
            'zadanie': task_detail}
    return render(request, 'taskdetails.html', data)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('tasks/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/tasks')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/tasks')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
