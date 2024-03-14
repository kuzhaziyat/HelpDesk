from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator
class User(AbstractUser):
    oname = models.CharField(blank = True, verbose_name = "Отчество")
    phone_regex = RegexValidator(regex = r'^\+?1?\d{9,11}$', message="Номер телефона должен быть введен в формате: '+7495200000'. Допускается до 11 цифр.")
    organization = models.ForeignKey('Organization',on_delete=models.PROTECT,verbose_name = "Организация",default = '',null=True)
    department = models.ForeignKey('Department',on_delete=models.PROTECT, verbose_name = "Отдел", default = '',null=True)
    telegramid = models.CharField( verbose_name = "id телеграмм пользователя",null=True)

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
    is_active = models.BooleanField("Активный", default = True,)   

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

class Department(models.Model):
    name = models.CharField("Наименование",max_length= 255,blank = False,)
    description = models.CharField("Описание",max_length= 255,blank = True)  
    is_active = models.BooleanField("Активный", default = True,)   
    organization = models.ForeignKey('Organization',on_delete=models.PROTECT,verbose_name = "Организация",default = '',null=True)

    def __str__(self):
        if self.organization:
            return self.name + " " + str(self.organization)
        else:
            return self.name
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'