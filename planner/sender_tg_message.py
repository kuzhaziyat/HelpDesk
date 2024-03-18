from task.models import *
from user.models import *
from .handler_bot import *

def mailing_by_timer():
    print('сработало')
    for obj in User.objects.all():
        # for task in Task.objects.filter(executor = obj):
            tasks = Task.objects.filter(executor = obj).exclude(sostoyan = Task.SOSTOYAN_CHOISEC['Closed'])
            orgTasks = Task.objects.filter(organization = obj.organization)
            notPrinTasks = Task.objects.filter(organization = obj.organization, status = Task.STATUS_CHOISEC['Zapl'])
            sendMessageTG(obj.telegramid,
                          'Здраствуйте, у вас\n' +
                          str(tasks.count()) +
                          ' заявок в работе,\n' +
                          str(orgTasks.count()) +
                          ' заявок у организации\n' +
                          str(notPrinTasks.count()) +
                          ' не принятых заявок\n\n' +
                          'посмотреть заявки можете по ссылке http://127.0.0.1:8000/task/task/'
                          )