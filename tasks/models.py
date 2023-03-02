from django.db import models
from django.contrib.auth.models import User


TASK_STATUS = (
    ('unresolved', 'Nie rozwiazano'),
    ('solved', 'Rozwiazano')
)


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(choices=TASK_STATUS, default='', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # musiałem usunąć ręcznie wartość unikalną
    expiry_date = models.DateField()

    class Meta:
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"
