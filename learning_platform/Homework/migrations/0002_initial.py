# Generated by Django 4.2.10 on 2024-04-10 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Homework', '0001_initial'),
        ('Students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Students.student'),
        ),
    ]
