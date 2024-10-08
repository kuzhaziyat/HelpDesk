from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,Group
from django import forms
from planner import handler_bot
from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = ()
    list_display_links = ['id','last_name','first_name', 'oname']
    list_display = ['id','last_name','first_name', 'oname', 'department', 'username']
    fieldsets = (
        (None, {
            'fields': ('username', 'password','last_login')
        }),
        ('Персональная информация', {
            'fields': ('last_name','first_name', 'oname','email','telegramid')
        }),
        ('Место работы', {
            'fields': ('organization','department','position','is_active','notes','groups')
        }),
    )

    

    def save_model(self, request, obj, form,change):
        if form.is_valid():
            handler_bot.sendMessageTG(obj.telegramid,'Ваш аккаунт привязали к сервису HelpDesk')
            if not obj.id and not request.user.is_superuser:
                obj.organization = request.user.organization
            if obj.is_active:
                obj.is_staff = True
                obj.save()   
            else:
                obj.is_staff = False
                obj.save()
            super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(CustomUserAdmin, self).get_queryset(request)
        else:
            qs = super(CustomUserAdmin, self).get_queryset(request)
            return qs.filter(organization=request.user.organization)

class DepartmentInlane(admin.TabularInline):
    model = Department
    extra = 0
    can_delete = False
    fields = ('name','description','is_active')
    show_change_link = True


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    can_delete = False
    user_fieldsets = (
        (None, {
            'fields': ('name','description','is_active')
        }),
    )
    readonly_fields = ['organization']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(DepartmentAdmin, self).get_queryset(request)
        else:
            qs = super(DepartmentAdmin, self).get_queryset(request)
            return qs.filter(organization=request.user.organization)
    
    def save_model(self, request, obj, form,change):
        if form.is_valid():
            if not obj.id:
                obj.organization = request.user.organization
                obj.save()
        super().save_model(request, obj, form, change)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    can_delete = False
    user_fieldsets = (
        (None, {
            'fields': ('name','description','is_active')
        }),
    )
    inlines = [DepartmentInlane]
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(OrganizationAdmin, self).get_queryset(request)
        else:
            qs = super(OrganizationAdmin, self).get_queryset(request)
            return qs.filter(name=request.user.organization, is_active = True)

