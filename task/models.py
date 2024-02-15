from django.db import models
from user import models as userModel
from colorfield.fields import ColorField

class Task(models.Model):
    name = models.CharField('Тема',max_length= 255)
    description = models.TextField('Описание',max_length= 255,blank=True)
    requester = models.ForeignKey(userModel.User,on_delete=models.PROTECT,verbose_name = "Отправитель",blank=True,null=True, related_name= 'task_requester'   ,limit_choices_to={'is_active': True})
    еxecutor = models.ForeignKey(userModel.User,on_delete=models.PROTECT,verbose_name = "Ответственный", related_name= 'task_executor',blank=True,null=True,limit_choices_to={'is_active': True})
    оrganization = models.ForeignKey(userModel.Organization,on_delete=models.PROTECT,verbose_name = "Организация",blank=True, null=True)
    division = models.ForeignKey(userModel.Division,on_delete=models.PROTECT,verbose_name = "Подразделение", null=True)
    department = models.ForeignKey(userModel.Department,on_delete=models.PROTECT,verbose_name = "Отдел",blank=True, null=True)
    typeTask = models.ForeignKey('TypeTask',on_delete=models.PROTECT,verbose_name = "Тип заявки", null=True)#
    status = models.ForeignKey('Status',on_delete=models.PROTECT,verbose_name = "Статус заявки",blank=True, null=True)#
    priority = models.ForeignKey('Priority',on_delete=models.PROTECT,verbose_name = "Приоритет заявки", null=True)#
    created_date = models.DateTimeField('Дата создания',auto_now_add=True)
    updated_date = models.DateTimeField('Дата обновления',auto_now=True)
    date_plan = models.DateTimeField('Плановая дата решения',blank=True, null=True)
    date_fact_completion = models.DateTimeField('Дата фактического выполнения',blank=True, null=True)#
    file_task = models.FileField("Файлы", upload_to=None, max_length=100, null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

class TypeTask(models.Model):
    name = models.CharField('Название')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'

class Status(models.Model):
    name = models.CharField('Название')
    color = ColorField(format="rgb")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'

class Priority(models.Model):
    name = models.CharField('Название')
    color = ColorField(format="rgb")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Приоритет заявки'
        verbose_name_plural = 'Приоритеты заявок'

class Comments(models.Model):
    description = models.TextField('Комментарий',max_length= 255)
    comment_creator = models.ForeignKey(userModel.User,on_delete=models.PROTECT,verbose_name = "Отправитель", related_name= 'comment_creator')
    created_date = models.DateTimeField('Дата создания',auto_now_add=True)
    task_id = models.ForeignKey("Task", verbose_name=("Комментарии"), on_delete=models.PROTECT)