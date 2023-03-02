from django.contrib import admin
from .models import *

# # Register your models here.
# admin.site.register(Task)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'description', 'user', 'status', 'expiry_date']
    list_filter = ['user','status', 'expiry_date']
