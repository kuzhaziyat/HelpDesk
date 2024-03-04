# Generated by Django 5.0.2 on 2024-02-28 08:13

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=255, verbose_name='Комментарий')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='rgb(255, 255, 255)', image_field=None, max_length=25, samples=None)),
            ],
            options={
                'verbose_name': 'Приоритет заявки',
                'verbose_name_plural': 'Приоритеты заявок',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тема')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='Описание')),
                ('status', models.CharField(blank=True, max_length=20, verbose_name='Статус')),
                ('sostoyan', models.CharField(blank=True, max_length=8, verbose_name='Состояние')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('date_plan', models.DateTimeField(blank=True, null=True, verbose_name='Плановая дата решения')),
                ('date_fact_completion', models.DateTimeField(blank=True, null=True, verbose_name='Дата фактического выполнения')),
                ('file_task', models.FileField(blank=True, null=True, upload_to=None, verbose_name='Файлы')),
                ('report_еxecutor', models.TextField(blank=True, max_length=255, verbose_name='Отчет о проделанной работе')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='TypeTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип заявки',
                'verbose_name_plural': 'Типы заявок',
            },
        ),
    ]
