# Generated by Django 5.0.2 on 2024-03-06 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Заявку', 'verbose_name_plural': 'Заявки'},
        ),
    ]
