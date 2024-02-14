from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,Group
from django import forms

from .models import *

<<<<<<< HEAD

=======
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
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
            'fields': ('department','post')
        }),
        ('Права доступа', {
            'fields': (
                'is_active',
                'groups', 
                )
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    def save_model(self, request, obj, form,change):
        if form.is_valid():
            # if(obj.post == 'director'):
            #     group = Group.objects.get(name='Директор') 
            #     group.user_set.add(obj.id)
            #     obj.save()
            if obj.is_active:
                obj.is_staff = True
                obj.save()   
            else:
                obj.is_staff = False
                obj.save()

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

class DepartmentInlane(admin.TabularInline):
    model = Department
    extra = 0
    can_delete = False
    fields = ('name','description','is_active')
    show_change_link = True

<<<<<<< HEAD
class DivisionInlane(admin.TabularInline):
    model = Division
    extra = 0
    can_delete = False
    fields = ('name','description','is_active')
    show_change_link = True    

=======
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
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
<<<<<<< HEAD
    
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
=======

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
    can_delete = False
    user_fieldsets = (
        (None, {
            'fields': ('name','description','is_active','division')
        }),
    )
<<<<<<< HEAD
    inlines = [DivisionInlane]
    
=======

>>>>>>> e79d23115a47bde3304ac22fd24fba651f3a233c
