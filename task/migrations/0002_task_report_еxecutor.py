# Generated by Django 5.0.2 on 2024-02-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='report_еxecutor',
            field=models.TextField(blank=True, max_length=255, verbose_name='Описание'),
        ),
    ]
