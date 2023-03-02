from django.shortcuts import render
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
            recipient = "kamilobroslak2@gmail.com"  # mail do testów formy maila
            #  recipient = i.user_id(User.email_user)
            password = ""  # przy wpisaniu hasła do konta google maile wychodzą i nie pojawia się błąd
            subject = "Masz niedokonczone zadania"
            content = """<h1>Masz niedokonczone zadania</h1>
                        <b>Sprawdz zadania przypisane do Ciebie.</b>
                        W załączniku plik"""

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


def tasks(request):
    tasks = Task.objects.all()
    data = {'zadania': tasks}
    return render(request, 'tasks.html', data)


def users(request):
    users = User.objects.all()
    data = {'uzytkownicy': users}
    return render(request, 'users.html', data)


def taskuser(request, id):
    user_tasks = User.objects.get(pk=id)
    user_task = Task.objects.filter(user_id=user_tasks)
    tasks = Task.objects.all()
    data = {'wybor_uzytkownika': user_tasks,
            'zadania_uzytkownika': user_task,
            'wszystkie': tasks}
    return render(request, 'taskuser.html', data)
