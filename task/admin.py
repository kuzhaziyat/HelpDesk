from typing import Any
from django.contrib import admin
from .models import *
<<<<<<< HEAD
from user import models as userModel
=======
from .task_services import  *

>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
class CommentInlane(admin.TabularInline):
    model = Comments
    extra = 0
    can_delete = False
    readonly_fields = ['created_date']

    fields = [('description',),('comment_creator',)]
    show_change_link = True
    
<<<<<<< HEAD
class DepartmentFilter(admin.SimpleListFilter):
    title = 'department' 
    parameter_name = 'department'
    def lookups(self, request , model_admin):
        print('sdasd')
        if 'division__id__exact' in request.GET:
            chapters = set([c.department for c in model_admin.model.objects.all().filter(division=id)])
        else:
            chapters = set([c.department for c in model_admin.model.objects.all()])

        return [(b.id, b.name) for b in chapters]     
    def queryset(self, request, queryset):   
        if self.value(): 
            return queryset.filter(department__id__exact=self.value())

class TaskAdmin(admin.ModelAdmin):
    
    readonly_fields = ['created_date','updated_date',]
    fieldsets  = (
=======
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date','updated_date']
    user_fieldsets  = (
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
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
<<<<<<< HEAD
    inlines = [CommentInlane]
    # def save_model(self, request, obj, form,change):
    #     print(obj.еxecutor)
    #     # if obj.requester == '':
    #     #     obj.requester = request.user
    #     #     obj.save()
            
=======
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(TaskAdmin, self).get_fieldsets(request, obj)
        return self.user_fieldsets   
    
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c

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
