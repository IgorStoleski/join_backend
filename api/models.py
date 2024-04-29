from django.db import models
from django.contrib.auth.models import User 

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20)
    priority = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title}"
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True, blank=True)  # Erlaube NULL-Werte
    number = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}"
    

class Subtask(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.title}"