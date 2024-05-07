from django.db import models
from django.contrib.auth.models import User 
from django.contrib.postgres.fields import ArrayField

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    status = models.CharField(max_length=20)
    category = models.CharField(max_length=20, null=True, blank=True)
    priority = models.CharField(max_length=20, null=True, blank=True)
    assignedTo = models.JSONField(null=True, blank=True)
    bgcolor = models.JSONField(blank=True)
    subtasks = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}"
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True, blank=True) 
    telefon = models.CharField(max_length=30, null=True, blank=True)
    bgcolor = models.CharField(max_length=7, default="#0038FF", blank=True)

    
    def __str__(self):
        return f"{self.name}"
    

class Subtask(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.title}"