# Generated by Django 5.0.2 on 2024-02-16 05:32

import colorfield.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0004_alter_user_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='rgb(255, 255, 255)', image_field=None, max_length=25, samples=None)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.organization', verbose_name='Организация')),
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
                ('color', colorfield.fields.ColorField(default='rgb(255, 255, 255)', image_field=None, max_length=25, samples=None)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.organization', verbose_name='Организация')),
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
                ('description', models.TextField(blank=True, max_length=255, verbose_name='Описание')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('date_plan', models.DateTimeField(blank=True, null=True, verbose_name='Плановая дата решения')),
                ('date_fact_completion', models.DateTimeField(blank=True, null=True, verbose_name='Дата фактического выполнения')),
                ('file_task', models.FileField(blank=True, null=True, upload_to=None, verbose_name='Файлы')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.department', verbose_name='Отдел')),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='user.division', verbose_name='Подразделение')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='task_org', to='user.organization', verbose_name='Организация')),
                ('priority', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='task.priority', verbose_name='Приоритет заявки')),
                ('requester', models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='task_requester', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='task.status', verbose_name='Статус заявки')),
                ('еxecutor', models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='task_executor', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=255, verbose_name='Комментарий')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('comment_creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_creator', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='task.task', verbose_name='Комментарии')),
            ],
        ),
        migrations.CreateModel(
            name='TypeTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.organization', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Тип заявки',
                'verbose_name_plural': 'Типы заявок',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='typeTask',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='task.typetask', verbose_name='Тип заявки'),
        ),
    ]
