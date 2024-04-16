from django.db import models
from django.contrib.auth.models import User 

class Todo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=150)
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.BooleanField(default=False)
    
    
    
