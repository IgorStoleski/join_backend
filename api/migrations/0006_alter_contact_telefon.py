# Generated by Django 5.0.4 on 2024-04-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_contact_telefon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='telefon',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
