# Generated by Django 5.0.4 on 2024-05-02 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_task_assignedto_alter_task_subtasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
