from django.http import HttpResponse
import json
from task.models import *
from user.models import *
from django.http import JsonResponse


from django.contrib.auth import authenticate, login

def get_list_task_for_tg_user(request, tgid):
    tgUser = User.objects.filter(telegramid = tgid)
    tasks = Task.objects.filter(executor = tgid).exclude(sostoyan = Task.SOSTOYAN_CHOISEC['Closed'])

    data = {'slug': tgid, 'message': '{tasks}'.format(tgid)}
    print(data)
    return HttpResponse(data)

def get_executor(request,dep_id):
    executor = User.objects.filter(department = dep_id, is_active = True)
    data = model_to_json(executor)
    return JsonResponse(data,safe=False)    

def get_department(request,org_id):
    department = Department.objects.filter(organization = org_id, is_active = True)
    data = model_to_json(department)
    return JsonResponse(data,safe=False)  

def model_to_json(queryset):
    data = {}
    data['queryset'] = []
    for i in queryset:
        data['queryset'].append({
            'name': i.__str__(),
            'pk': i.pk
        })
    return data