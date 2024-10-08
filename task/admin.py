from typing import Any, Mapping
from django.contrib import admin
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from user import models as userModel
from django import forms
from django.utils.html import format_html
from django.db.models import Q
from django.http import HttpResponseRedirect,JsonResponse
import requests
from django.contrib import messages
from django.utils import timezone

from planner import handler_bot

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display_links = ['name']
    change_form_template = "task/taskadmin_change_form.html"
    read_only_fields = True

    def response_change(self, request, obj):
        if "_prin" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['InWork']
            obj.status = self.model.STATUS_CHOISEC['Prin']
            obj.organization = request.user.organization
            obj.department = request.user.department
            obj.executor = request.user
            handler_bot.sendMessageTG(obj.executor.telegramid,'Вы взяли в работу заявку под номером ' + str(obj.id))
            handler_bot.sendMessageTG(obj.requester.telegramid,'Вашу заявку под номером ' + str(obj.id) + ' взяли в работу')
            obj.save()
            self.message_user(request, "Заявка взята в работу")
            return HttpResponseRedirect(".")
        if "_canceled" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Closed']
            obj.status = self.model.STATUS_CHOISEC['Canceled']
            handler_bot.sendMessageTG(obj.executor.telegramid,'Заявку под номером ' + str(obj.id) + ' отменили')
            obj.save()
            self.message_user(request, "Заявка отменена")
            return HttpResponseRedirect(".")
        if "_ready" in request.POST:
            if obj.report_executor:
                if obj.department:
                    if obj.executor:
                        # obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Closed']
                        obj.status = self.model.STATUS_CHOISEC['Vipol']
                        obj.date_fact_completion = timezone.now()
                        handler_bot.sendMessageTG(obj.requester.telegramid,'Вашу заявку под номером ' + str(obj.id) + ' выполнили, войдите в систему и проверьте Отчет о проделанной работе')
                        obj.save()
                        self.message_user(request, "Статус заявки выполнена")
                        return HttpResponseRedirect(".")
                    else:
                        messages.error(request, "Вы не заполнили Ответсвенного исполнителя")
                        return HttpResponseRedirect(".")

                else:
                    messages.error(request, "Вы не заполнили отдел исполнителя")
                    return HttpResponseRedirect(".")

            else:
                messages.error(request, "Вы не заполнили Отчет о проделанной работе")
                return HttpResponseRedirect(".")


        if "_send_control" in request.POST:
            if obj.controluser:
                obj.sostoyan = self.model.SOSTOYAN_CHOISEC['InWork']
                obj.status = self.model.STATUS_CHOISEC['InControl']
                handler_bot.sendMessageTG(obj.controluser.telegramid,'К вам на контроль отправили заявку под номером ' + str(obj.id))
                if obj.executor:
                    handler_bot.sendMessageTG(obj.executor.telegramid,'Заявка под номером ' + str(obj.id) + ' отправлена на контроль')
                obj.save()
                self.message_user(request, "Заявка отправлена на контроль")
            else:
                messages.error(request, "Вы не добавили Контролирующего сотрудника")
            return HttpResponseRedirect(".")
        if "_send_in_work" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['InWork']
            obj.status = self.model.STATUS_CHOISEC['Return']
            obj.controluser = any
            handler_bot.sendMessageTG(obj.executor.telegramid,'Заявка под номером ' + str(obj.id) + ' возвращена в работу')
            handler_bot.sendMessageTG(obj.requester.telegramid,'Вашу заявку под номером ' + str(obj.id) + ' вернули в работу')
            obj.save()
            self.message_user(request, "Заявка возвращена в работу")
            return HttpResponseRedirect(".")
        if "_control_ready" in request.POST:
            # obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Closed']
            obj.status = self.model.STATUS_CHOISEC['Control']
            handler_bot.sendMessageTG(obj.requester.telegramid,'Заявку под номером ' + str(obj.id) + ' выполнили, войдите в систему и проверьте Отчет о проделанной работе')
            obj.save()
            self.message_user(request, "Статус заявки выполнена")
            return HttpResponseRedirect(".")
        if '_closed' in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Closed']
            handler_bot.sendMessageTG(obj.controluser.telegramid,'Заявку под номером ' + str(obj.id) + ' закрыта')
            if obj.executor:
                handler_bot.sendMessageTG(obj.executor.telegramid,'Заявка под номером ' + str(obj.id) + ' закрыта')
            obj.save()
            self.message_user(request, "Состояние заявки закрыта")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def color_priority(self, obj):
        if obj.priority:
            return format_html('<p style="color:{}">{}</span>', obj.priority.color, obj.priority)
    
    color_priority.short_description = 'Приоритет'

    color_priority.allow_tags = True

    list_display = ('id','name','typeTask','status','sostoyan','color_priority','department','date_plan')

    fieldsets  = (
        ('Основные данные заявки',{
            'fields': [ 
                        ('name'),
                        ('description','file_task'),
                        ('typeTask','priority','date_plan'),
                        ('status','sostoyan',),
                       ]
        }),
        ('Исполнитель',{
            'fields':[
                ('organization','department'),
                ('executor','report_executor'),
            ]
        }),
        ('Дополнительные поля',{
            'fields': [ 
                        ('requester','controluser'),             
                        ('created_date','updated_date','date_fact_completion'), 
                       ]
        })
    )

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False 
        return formfield
    
    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        obj = self.get_object(object_id= object_id,request=request)
        if object_id:
            extra_context = extra_context or {}
            extra_context = {'obj': obj, "request": request,"self": self}

        if obj.requester == request.user or request.user.is_superuser:
            pass
        else:    
            extra_context = extra_context or {}
            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_and_chandes'] = True    
        return super().change_view(
                request, object_id, form_url, extra_context=extra_context,
            )

    def get_readonly_fields(self, request, obj=None):
        readonly_requester = ('created_date','status',
                              'sostoyan','updated_date',
                              'date_fact_completion','requester',
                              'report_executor'
                              )
        
        readonly_controluser = ('created_date','status',
                                'sostoyan','updated_date',
                                'date_fact_completion','requester'
                                )
        
        readonly_executor = ('created_date','status',
                        'sostoyan','updated_date',
                        'date_fact_completion','requester',
                        'name', 'description', 'controluser',
                        'organization', 'typeTask', 'priority',
                        'file_task', 'date_plan','executor','department'
                        )

        readonly_all = ('created_date','status',
                        'sostoyan','updated_date',
                        'date_fact_completion','requester',
                        'name', 'description', 'controluser',
                        'organization', 'typeTask', 'priority',
                        'file_task', 'date_plan',
                        'report_executor','executor','department'
                        )

        if obj is not None:
            if request.user == obj.requester:
                return readonly_requester
            elif request.user == obj.controluser:
                return readonly_controluser
            elif request.user == obj.executor:
                return readonly_executor
            else:
                return readonly_all
        else:
            return readonly_requester

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.requester == request.user or request.user.is_superuser:
                return True
            else:
                return False

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.sostoyan in self.model.SOSTOYAN_CHOISEC['Closed']:
                print(obj.sostoyan)
                return False
            return True

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not obj.id:
                obj.status = self.model.STATUS_CHOISEC['Zapl']
                obj.requester = request.user
                obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Opened']
                if obj.executor:
                    handler_bot.sendMessageTG(obj.executor.telegramid,'В заявке под номером ' + str(obj.id) + ' вас сделали ответсвенным')
                obj.save()
            if not obj.organization:
                obj.organization = request.user.organization
                obj.save()
            obj.save()
        super().save_model(request, obj, form, change)

    # def get_fieldsets(self, request, obj=None):
    #      if request.user.is_superuser:
    #          return super(TaskAdmin, self).get_fieldsets(request, obj)
    #      return self.user_fieldsets   

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TaskAdmin, self).get_queryset(request)
        else:
            qs = super(TaskAdmin, self).get_queryset(request)
            return qs.filter(Q(organization=request.user.organization) | Q(requester=request.user))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "typeTask":
            kwargs["queryset"] = TypeTask.objects.filter(organization=request.user.organization)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(TypeTask)
class TypeTaskAdmin(admin.ModelAdmin):
    user_fieldsets = (
        (None, {
            'fields': [('name')]
        }),
    )
    readonly_fields = ['organization']

    def save_model(self, request, obj, form,change):
        if form.is_valid():
            if not obj.id:
                obj.organization = request.user.organization
                obj.save()
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TypeTaskAdmin, self).get_queryset(request)
        else:
            qs = super(TypeTaskAdmin, self).get_queryset(request)
            return qs.filter(organization=request.user.organization)
            
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(TypeTaskAdmin, self).get_fieldsets(request, obj)
        return self.user_fieldsets

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):

    def color_priority(self, obj):
        return format_html('<span style="width:50%;height:15px;display:block;background-color:{}"></span>', obj.color)
    
    color_priority.short_description = 'Цвет'
    color_priority.allow_tags = True

    list_display = ('name', 'color_priority')
    fieldsets  = (
        (None,{
            'fields': ('name', 'color')
        }),
    )
