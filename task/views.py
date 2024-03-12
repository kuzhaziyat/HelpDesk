from django.http import HttpResponse
from task.models import *
from user.models import *
from django.http import JsonResponse


from django.contrib.auth import authenticate, login

def get_list_task_for_tg_user(request, tgid):
    tgUser = User.objects.filter(telegramid = tgid)
    tasks = Task.objects.filter(еxecutor = tgid).exclude(sostoyan = Task.SOSTOYAN_CHOISEC['Closed'])

    data = {'slug': tgid, 'message': '{tasks}'.format(tgid)}
    print(data)
    return HttpResponse(data)

def get_department(request,org_id):
    print('request')
    organization_id = request.GET.get('organization')
    departments = Department.objects.filter(organization = organization_id).values('id','name')
    return JsonResponse(list(departments),safe=False)    