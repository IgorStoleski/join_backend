from django.db import models
from django.contrib.auth.models import User 
from django.contrib.postgres.fields import ArrayField

class Task(models.Model):
    """
    A class representing a task.
    Attributes:
        title (str): The title of the task.
        description (str): The description of the task.
        due_date (datetime.date): The due date of the task.
        status (str): The status of the task.
        category (str, optional): The category of the task. Defaults to None.
        priority (str, optional): The priority of the task. Defaults to None.
        assignedTo (JSON, optional): JSON field representing users assigned to the task. Defaults to None.
        bgcolor (JSON, optional): JSON field representing background color settings. Defaults to None.
        subtasks (JSON, optional): JSON field representing subtasks. Defaults to None.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
        """
        Returns a string representation of the task.
        Returns:
            str: The title of the task.
        """
        return f"{self.title}"
    
    
class Contact(models.Model):
    """
    Represents a contact with attributes such as name, surname, email, telephone, and background color.
    Attributes:
        name (str): The name of the contact.
        surname (str): The surname of the contact.
        email (str): The email address of the contact. Can be null.
        telefon (str): The telephone number of the contact. Can be null.
        bgcolor (str): The background color associated with the contact. Default is "#0038FF".
    """
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True, blank=True) 
    telefon = models.CharField(max_length=30, null=True, blank=True)
    bgcolor = models.CharField(max_length=7, default="#0038FF", blank=True)

    
    def __str__(self):
        """
        Returns a string representation of the contact.
        Returns:
            str: The name of the contact.
        """
        return f"{self.name}"
    

class Subtask(models.Model):
    """
    Represents a subtask in a task management system.
    Attributes:
        title (str): The title of the subtask.
    """
    title = models.CharField(max_length=100)
    
    def __str__(self):
        """
        Returns a string representation of the subtask.
        Returns:
            str: The title of the subtask.
        """
        return f"{self.title}"