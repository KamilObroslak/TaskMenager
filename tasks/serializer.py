from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user_id', 'status', 'expiry_date']
        #  przy fields zamiast user to musiałem dodać user_id zgodnie z tym jaki tytuł
        #  kolumny jest w bazie
