# Generated by Django 5.0.2 on 2024-02-18 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_creator', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.AddField(
            model_name='priority',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.organization', verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='status',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.organization', verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='task',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.department', verbose_name='Отдел'),
        ),
        migrations.AddField(
            model_name='task',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='task_org', to='user.organization', verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='task.priority', verbose_name='Приоритет заявки'),
        ),
        migrations.AddField(
            model_name='task',
            name='requester',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='task_requester', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.AddField(
            model_name='task',
            name='еxecutor',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='task_executor', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный'),
        ),
        migrations.AddField(
            model_name='comments',
            name='task_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='task.task', verbose_name='Комментарии'),
        ),
        migrations.AddField(
            model_name='typetask',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.organization', verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='task',
            name='typeTask',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='task.typetask', verbose_name='Тип заявки'),
        ),
    ]
