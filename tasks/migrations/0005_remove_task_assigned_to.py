# Generated by Django 5.1.2 on 2024-11-12 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_to',
        ),
    ]
