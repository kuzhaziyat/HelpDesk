from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

POST_CHOICES = {
    "director": "Директор",
    "HR": "Работник отдела кадров",
    "headDivisin": "Руководитель подразделения",
    "headDepartment": "Начальник отдела",
    "orker": "Сотрудник",

}

class User(AbstractUser):
    oname = models.CharField(blank = True, verbose_name = "Отчество")
    phone_regex = RegexValidator(regex = r'^\+?1?\d{9,11}$', message="Номер телефона должен быть введен в формате: '+7495200000'. Допускается до 11 цифр.")
    phone_number = models.CharField(validators=[phone_regex], max_length = 17, blank = True, verbose_name = "Телефон") 
    оrganization = models.ForeignKey('Organization',on_delete=models.PROTECT,verbose_name = "Организация",default = '',null=True)
    department = models.ForeignKey('Department',on_delete=models.PROTECT,verbose_name = "Отдел", default = '',null=True)
    group = models.OneToOneField('auth.Group', unique=True, on_delete=models.PROTECT,related_name='+',null=True,verbose_name = "Должность")

    def __str__(self):
        return (self.last_name + ' ' 
                + self.first_name + ' ' 
                + self.oname 
                )
    class Meta: 
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'    

class Organization(models.Model):
    name = models.CharField("Наименование",max_length= 255,blank = False)
    description = models.CharField("Описание",max_length= 255,blank = True)  
    is_active = models.BooleanField(default = True,)   

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

class Division(models.Model):
    name = models.CharField("Наименование",max_length= 255,blank = False,)
    description = models.CharField("Описание",max_length= 255,blank = True)  
    is_active = models.BooleanField(default = True,)   
    оrganization = models.ForeignKey('Organization',on_delete=models.PROTECT,verbose_name = "Организация",default = '',null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Department(models.Model):
    name = models.CharField("Наименование",max_length= 255,blank = False,)
    description = models.CharField("Описание",max_length= 255,blank = True)  
    is_active = models.BooleanField(default = True,)   
    division = models.ForeignKey(Division,on_delete=models.PROTECT,default = '', verbose_name = 'Подразделение')


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'