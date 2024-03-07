from typing import Any
from django.contrib import admin
from .models import *
from user import models as userModel
from django.utils.html import format_html
from django.db.models import Q
from django.http import HttpResponseRedirect
import requests
from django.contrib import messages

from planner import handler_bot
# Добавление пути к папке с вашим модулем в переменную PYTHONPATH

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedSpecificationForm, self).__init__(*args, **kwargs)
        self.fields['item_types'].widget = forms.CheckboxSelectMultiple(
            choices=Item.TypeChoice.feed_specification_choices()
        )
        try:
            self.fields['tags'].queryset = Tag.objects.filter(
                station=self.instance.feed.station
            )
            self.fields['video_tags'].queryset = VideoTag.objects.filter(
                station=self.instance.feed.station
            )
        except:
            self.fields['tags'].queryset = Tag.objects.none()
            self.fields['video_tags'].queryset = VideoTag.objects.none()
    
    def _clean_fields(self):
        self.fields['tags'].queryset = Tag.objects.filter(station_id=self.data['station'])
        self.fields['video_tags'].queryset = VideoTag.objects.filter(station_id=self.data['station'])
        super()._clean_fields()

class CommentInlane(admin.StackedInline):
    model = Comments
    extra = 0
    can_delete = False
    readonly_fields = ['created_date','comment_creator']

    fields = [('description','created_date','comment_creator'),]
    def save_model(self, request, obj, form,change):
        if form.is_valid():
            if not obj.id:
                obj.comment_creator = request.user
                obj.save()
        super().save_model(request, obj, form, change)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    change_form_template = "task/taskadmin_change_form.html"
    read_only_fields = True

    def response_change(self, request, obj):
        if "_prin" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['InWork']
            obj.status = self.model.STATUS_CHOISEC['Prin']
            obj.еxecutor = request.user
            handler_bot.sendMessageTG(obj.еxecutor.telegramid,'Вы взяли в работу заявку под номером ' + str(obj.id))
            handler_bot.sendMessageTG(obj.requester.telegramid,'Вашу заявку под номером ' + str(obj.id) + ' взяли в работу')
            obj.save()
            self.message_user(request, "Заявка взята в работу")
            return HttpResponseRedirect(".")
        if "_canceled" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Closed']
            obj.status = self.model.STATUS_CHOISEC['Canceled']
            handler_bot.sendMessageTG(obj.еxecutor.telegramid,'Заявку под номером ' + str(obj.id) + ' отменили')
            obj.save()
            self.message_user(request, "Заявка отменена")
            return HttpResponseRedirect(".")
        if "_ready" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Closed']
            obj.status = self.model.STATUS_CHOISEC['Vipol']
            handler_bot.sendMessageTG(obj.requester.telegramid,'Вашу заявку под номером ' + str(obj.id) + ' выполнили, войдите в систему и проверьте Отчет о проделанной работе')
            obj.save()
            self.message_user(request, "Заявка считается выполненной")
            return HttpResponseRedirect(".")
        if "_send_control" in request.POST:
            if obj.controluser:
                obj.sostoyan = self.model.SOSTOYAN_CHOISEC['InWork']
                obj.status = self.model.STATUS_CHOISEC['InControl']
                handler_bot.sendMessageTG(obj.controluser.telegramid,'К вам на контроль отправили заявку под номером ' + str(obj.id))
                if obj.еxecutor:
                    handler_bot.sendMessageTG(obj.еxecutor.telegramid,'Заявка под номером ' + str(obj.id) + ' отправлена на контроль')
                obj.save()
                self.message_user(request, "Заявка отправлена на контроль")
            else:
                messages.error(request, "Вы не добавили Контролирующего сотрудника")
            return HttpResponseRedirect(".")
        if "_send_in_work" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['InWork']
            obj.status = self.model.STATUS_CHOISEC['Return']
            obj.controluser = any
            handler_bot.sendMessageTG(obj.еxecutor.telegramid,'Заявка под номером ' + str(obj.id) + ' возвращена в работу')
            handler_bot.sendMessageTG(obj.requester.telegramid,'Вашу заявку под номером ' + str(obj.id) + ' вернули в работу')
            obj.save()
            self.message_user(request, "Заявка возвращена в работу")
            return HttpResponseRedirect(".")
        if "_control_ready" in request.POST:
            obj.sostoyan = self.model.SOSTOYAN_CHOISEC['Closed']
            obj.status = self.model.STATUS_CHOISEC['Control']
            handler_bot.sendMessageTG(obj.requester.telegramid,'Заявку под номером ' + str(obj.id) + ' выполнили, войдите в систему и проверьте Отчет о проделанной работе')
            obj.save()
            self.message_user(request, "Заявка считается выполненной")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def color_priority(self, obj):
        if obj.priority:
            return format_html('<p style="color:{}">{}</span>', obj.priority.color, obj.priority)
    
    color_priority.short_description = 'Приоритет'

    color_priority.allow_tags = True

    list_display = ('id','name','typeTask','status','sostoyan','color_priority','department','date_plan')
    readonly_fields = ['created_date','status','sostoyan','updated_date','date_fact_completion','requester']
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
                ('еxecutor','report_еxecutor'),
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
                obj.save()
            if not obj.organization:
                obj.organization = request.user.organization
                obj.save()
            obj.save()
        super().save_model(request, obj, form, change)

    # def get_fieldsets(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return super(TaskAdmin, self).get_fieldsets(request, obj)
    #     return self.user_fieldsets   

    def get_queryset(self, request):
        # if request.user.is_superuser:
        #     return super(TaskAdmin, self).get_queryset(request)
        # else:   
        qs = super(TaskAdmin, self).get_queryset(request)
        return qs.filter(Q(organization=request.user.organization) | Q(requester=request.user))

    inlines = [CommentInlane]

@admin.register(TypeTask)
class TypeTaskAdmin(admin.ModelAdmin):
    user_fieldsets = (
        (None, {
            'fields': [('name')]
        }),
    )
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

    readonly_fields = ['organization']

    list_display = ('name', 'color_priority')
    user_fieldsets  = (
        (None,{
            'fields': ('name', 'color')
        }),
    )
    def save_model(self, request, obj, form,change):
        if form.is_valid():
            if not obj.id:
                obj.organization = request.user.organization
                obj.save()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(PriorityAdmin, self).get_queryset(request)
        else:
            qs = super(PriorityAdmin, self).get_queryset(request)
            return qs.filter(organization=request.user.organization)            
        
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(PriorityAdmin, self).get_fieldsets(request, obj)
        return self.user_fieldsets
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    readonly_fields = ['comment_creator']

    def save_model(self, request, obj, form,change):
        if form.is_valid():
            if not obj.id:
                obj.comment_creator = request.user
                obj.save()
        super().save_model(request, obj, form, change)