from typing import Any
from django.contrib import admin
from .models import *
from user import models as userModel


class CommentInlane(admin.TabularInline):
    model = Comments
    extra = 0
    can_delete = False
    readonly_fields = ['created_date']

    fields = [('description',),('comment_creator',)]
    show_change_link = True
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date','updated_date']
    user_fieldsets  = (
        (None,{
            'fields': [ 
                        ('name', 'description'),
                        ('typeTask','status'),
                        ('priority', 'date_plan'),
                       ]
        }),
        ('Дополнительные поля',{
            'fields': [ 
                        ('еxecutor', 'requester'),
                        ('division','department'),                       
                        ('file_task'),
                        ('created_date','updated_date'),                       
                        ('date_reaction','date_fact_completion'), 
                       ]
        })
    )
    inlines = [CommentInlane]
    
    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.requester = request.user.id
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        return qs.filter(department=request.user.department or requester == request.user)  
    
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(TaskAdmin, self).get_fieldsets(request, obj)
        return self.user_fieldsets   
    

    inlines = [CommentInlane]

class TypeTaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    fieldsets  = (
        (None,{
            'fields': ('name', 'color')
        }),
    )
