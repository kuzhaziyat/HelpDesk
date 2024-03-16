from django.http import HttpResponse
from django.core import serializers
import json
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

def get_executor(request,dep_id):
    executor = User.objects.filter(department = dep_id) 
    qs_js = serializers.serialize('json', executor)
    print(str(qs_js))
    return JsonResponse(qs_js,safe=False)    

def get_department(request,org_id):
    department = Department.objects.filter(organization = org_id)
    qs_js = serializers.serialize('json', department)
    print(str(qs_js))
    return JsonResponse(qs_js,safe=False)  