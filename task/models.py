from django.db import models
from user import models as userModel
from colorfield.fields import ColorField

PRIORITY_CHOISEC = {
        "Opened": "Открыта",
        "InWork": "В работе",
        "Closed": "Закрыта",
    }

class Task(models.Model):
    STATUS_CHOISEC = {
    "Zapl": "Запланирована",
    "Prin": "Принята к исполнению",
    "Vipol": "Выполнена",
    "Canceled": "Отменена",
    "InControl": "На контроле",
    "Return": "Возвращена",
    "Control": "Проконтролирована",
    }
    SOSTOYAN_CHOISEC = {
        "Opened": "Открыта",
        "InWork": "В работе",
        "Closed": "Закрыта",
    }
    name = models.CharField('Тема',max_length= 255)
    description = models.TextField('Описание',max_length= 255,blank=True)
    requester = models.ForeignKey(userModel.User,on_delete=models.PROTECT,verbose_name = "Отправитель",blank=True,null=True, related_name= 'task_requester'   ,limit_choices_to={'is_active': True})
    controluser = models.ForeignKey(userModel.User,on_delete=models.PROTECT,verbose_name = "Контролирующий сотрудник",blank=True,null=True, related_name= 'task_controller'   ,limit_choices_to={'is_active': True})
    executor = models.ForeignKey(userModel.User,on_delete=models.PROTECT,verbose_name = "Ответственный", related_name= 'task_executor',blank=True,null=True,limit_choices_to={'is_active': True})
    organization = models.ForeignKey(userModel.Organization,on_delete=models.PROTECT,verbose_name = "Организация",blank=False, null=True,related_name= 'task_org')
    department = models.ForeignKey(userModel.Department,on_delete=models.PROTECT,verbose_name = "Отдел",blank=True, null=True)
    typeTask = models.ForeignKey('TypeTask',on_delete=models.PROTECT,verbose_name = "Тип заявки", null=True)#
    status = models.CharField(max_length=20,blank=True,verbose_name = "Статус")
    sostoyan = models.CharField(max_length=8,blank=True,verbose_name = "Состояние")
    priority = models.ForeignKey('Priority',on_delete=models.PROTECT,verbose_name = "Приоритет заявки", null=True)#
    created_date = models.DateTimeField('Дата создания',auto_now_add=True)
    updated_date = models.DateTimeField('Дата обновления',auto_now=True)
    date_plan = models.DateTimeField('Срок исполнении',blank=True, null=True)
    date_fact_completion = models.DateTimeField('Дата фактического выполнения',blank=True, null=True)#
    file_task = models.FileField("Файлы", upload_to=None, max_length=100, null=True,blank=True)
    report_executor = models.TextField('Отчет о проделанной работе',max_length= 255,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки'

class TypeTask(models.Model):
    name = models.CharField('Название')
    organization = models.ForeignKey(userModel.Organization,on_delete=models.PROTECT,verbose_name = "Организация",blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'
    
class Priority(models.Model):
    name = models.CharField('Название')
    color = ColorField(format="rgb")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Приоритет заявки'
        verbose_name_plural = 'Приоритеты заявок'
