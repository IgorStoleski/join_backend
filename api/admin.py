from django.contrib import admin
from .models import Task, Contact, Subtask

# Register your models here.
admin.site.register(Task)
admin.site.register(Contact)
admin.site.register(Subtask)