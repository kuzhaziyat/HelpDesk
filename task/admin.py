from typing import Any
from django.contrib import admin
from .models import *
from user import models as userModel
from django.utils.html import format_html

class CommentInlane(admin.TabularInline):
    model = Comments
    extra = 0
    can_delete = False
    readonly_fields = ['created_date']

    fields = [('description',),('comment_creator',)]
    show_change_link = True
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    read_only_fields = True

    def color_priority(self, obj):
        if obj.priority:
            return format_html('<p style="color:{}">{}</span>', obj.priority.color, obj.priority)
    
    color_priority.short_description = 'Приоритет'

    color_priority.allow_tags = True

    list_display = ('name','color_priority')

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
                ('еxecutor'),
            ]
        }),
        ('Дополнительные поля',{
            'fields': [ 
                        ('requester'),             
                        ('created_date','updated_date','date_fact_completion'), 
                       ]
        })
    )
    inlines = [CommentInlane]

    def imports(modeladmin, request, queryset):
        print("Imports button pushed")

    changelist_actions = ('imports', )

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False 
        return formfield
    
    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        obj = self.get_object(object_id= object_id,request=request)
        if obj.requester == request.user or request.user.is_superuser:
            pass
        else:    
            extra_context = extra_context or {}
            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_and_chandes'] = True    

        return super().changeform_view(request, object_id, form_url, extra_context)
    
    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.requester == request.user or request.user.is_superuser:
                return True
            else:
                return False
    
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
        if request.user.is_superuser:
            return super(TaskAdmin, self).get_queryset(request)
        else:   
            qs = super(TaskAdmin, self).get_queryset(request)
            return qs.filter(organization=request.user.organization)

    inlines = [CommentInlane]

@admin.register(TypeTask)
class TypeTaskAdmin(admin.ModelAdmin):
    readonly_fields = ['organization']
    user_fieldsets = (
        (None, {
            'fields': ('name')
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