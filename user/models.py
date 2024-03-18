from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator


class User(AbstractUser):
    oname = models.CharField(verbose_name = "Отчество")
    organization = models.ForeignKey('Organization',on_delete=models.PROTECT,verbose_name = "Организация",default = '',null=True)
    department = models.ForeignKey('Department',on_delete=models.PROTECT, verbose_name = "Отдел", default = '',null=True)
    telegramid = models.CharField( verbose_name = "id телеграмм пользователя",null=True, blank=True)
    position = models.CharField(verbose_name = 'Должность', null=True, blank=True)
    notes = models.TextField('Заметки к сотруднику',max_length= 255,blank=True)
    is_first_login = models.BooleanField(default=True)  

    def __str__(self):
        return (self.last_name + ' ' 
                + self.first_name + ' ' 
                + self.oname + ' ' 
                + str(self.position)
                )
    
    def __init__(self, *args, **kwargs):
        super(User,self).__init__(*args, **kwargs)
        self._meta.get_field('first_name').blank = False
        self._meta.get_field('last_name').blank = False
        self._meta.get_field('username').verbose_name = 'Номер телефона'
        self._meta.get_field('username').help_text = "Номер телефона должен быть введен в формате: '+7495200000'. Допускается до 11 цифр."
        self._meta.get_field('username').validators = [RegexValidator(regex = r'^\+?1?\d{9,11}$', message="Номер телефона должен быть введен в формате: '+7495200000'. Допускается до 11 цифр.")]
        self._meta.get_field('is_active').verbose_name = 'Работает'
        self._meta.get_field('is_active').help_text = "Отметьте, если сотрудник не работает. Уберите эту отметку чтобы отметить что сотрудник не работает(в отпуске, на больничном)."

    def natural_key(self):
        return (self.name, self.pk)

    class Meta: 
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'    

class Organization(models.Model):
    name = models.CharField("Полное наименование организации",max_length= 255,blank = False)
    ogrn = models.CharField("ОГРН",max_length=13,null=True, blank=False)
    INN = models.CharField("ИНН",max_length=12,null=True, blank=False)
    KPP = models.CharField("КПП",max_length=9,null=True, blank=False)
    yur_adres = models.CharField("Юридический адрес",max_length=255,null=True, blank=False)
    is_active = models.BooleanField("Активный",help_text='Уберите отметку чтобы Организация не выходил в списках', default = True,)   

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

class Department(models.Model):
    name = models.CharField("Наименование",max_length= 255,blank = False,)
    description = models.CharField("Описание",max_length= 255,blank = True)  
    is_active = models.BooleanField("Активный",help_text='Уберите отметку чтобы отдел не выходил в списках', default = True,)   
    organization = models.ForeignKey('Organization',on_delete=models.PROTECT,verbose_name = "Организация",default = '',null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'