<<<<<<< HEAD
# Generated by Django 5.0.2 on 2024-02-13 17:17
=======
# Generated by Django 5.0.2 on 2024-02-13 04:07
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c

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
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Статус заявки',
                'verbose_name_plural': 'Статусы заявок',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тема')),
<<<<<<< HEAD
                ('description', models.TextField(blank=True, max_length=255, verbose_name='Описание')),
=======
                ('description', models.TextField(max_length=255, verbose_name='Описание')),
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('date_plan', models.DateTimeField(blank=True, null=True, verbose_name='Плановая дата решения')),
                ('date_fact_completion', models.DateTimeField(blank=True, null=True, verbose_name='Дата фактического выполнения')),
                ('date_reaction', models.DateTimeField(blank=True, null=True, verbose_name='Время реагирования')),
<<<<<<< HEAD
                ('file_task', models.FileField(blank=True, null=True, upload_to=None, verbose_name='Файлы')),
=======
                ('file_task', models.FileField(null=True, upload_to=None, verbose_name='Файлы')),
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
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
