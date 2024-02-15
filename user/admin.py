from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,Group
from django import forms

from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'oname', 'phone_number','email')
        }),
        ('Место работы', {
            'fields': ('department','group')
        }),
        ('Права доступа', {
            'fields': (
                'is_active',
                )
        }),
    )
    
    def save_model(self, request, obj, form,change):
        if form.is_valid():
            if obj.is_active:
                obj.is_staff = True
                obj.save()   
            else:
                obj.is_staff = False
                obj.save()

class DepartmentInlane(admin.TabularInline):
    model = Department
    extra = 0
    can_delete = False
    fields = ('name','description','is_active')
    show_change_link = True

class DivisionInlane(admin.TabularInline):
    model = Division
    extra = 0
    can_delete = False
    fields = ('name','description','is_active')
    show_change_link = True    

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    can_delete = False

    user_fieldsets = (
        (None, {
            'fields': ('name','description','is_active')
        }),
    )
    inlines = [DepartmentInlane]
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    can_delete = False
    user_fieldsets = (
        (None, {
            'fields': ('name','description','is_active','division')
        }),
    )
    
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    can_delete = False
    user_fieldsets = (
        (None, {
            'fields': ('name','description','is_active','division')
        }),
    )
    inlines = [DivisionInlane]
    

