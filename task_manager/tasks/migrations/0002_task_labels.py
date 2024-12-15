# Generated by Django 5.1.2 on 2024-11-11 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(
                blank=True,
                related_name='tasks',
                to='labels.label'
            ),
        ),
    ]