# Generated by Django 4.2.10 on 2024-05-17 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='cost',
            field=models.IntegerField(default=500),
            preserve_default=False,
        ),
    ]