# Generated by Django 5.1.3 on 2024-12-05 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_rename_name_task_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='title',
            new_name='name',
        ),
    ]