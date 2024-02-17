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
    def color_status(self, obj):
        if obj.status:
            return format_html('<p style="color:{}">{}</span>', obj.status.color, obj.status)
    
    def color_priority(self, obj):
        if obj.priority:
            return format_html('<p style="color:{}">{}</span>', obj.priority.color, obj.priority)
    
    color_priority.short_description = 'Приоритет'
    color_status.short_description = 'Статус'

    color_priority.allow_tags = True
    color_status.allow_tags = True

    list_display = ('name', 'color_status','color_priority')

    readonly_fields = ['created_date','status','updated_date','date_fact_completion','requester']
    fieldsets  = (
        (None,{
            'fields': [ 
                        ('name', 'description'),
                        ('typeTask','status'),
                        ('priority', 'date_plan'),
                        ('department'), 
                       ]
        }),
        ('Дополнительные поля',{
            'fields': [ 
                        ('requester','еxecutor'),             
                        ('file_task','organization'),
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
        print(request.user.organization)
        if form.is_valid() and not obj.id:
            obj.status = Status(id = 4)
            obj.requester = request.user
            obj.organization = request.user.organization
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
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    def color_status(self, obj):
        return format_html('<span style="width:50%;height:15px;display:block;background-color:{}"></span>', obj.color)
    
    color_status.short_description = 'Цвет'
    color_status.allow_tags = True

    list_display = ('name', 'color_status')
    fieldsets  = (
        (None,{
            'fields': ('name', 'color')
        }),
    )

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
