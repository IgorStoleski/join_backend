# Generated by Django 5.0.4 on 2024-04-30 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_task_assignedto_task_bgcolor_task_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]
