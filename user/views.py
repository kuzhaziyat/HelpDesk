import json
from .models import User
from django.shortcuts import render
from .forms import *
from django.http import JsonResponse

def is_first_login(request):
	user = request.user
	if(not user.is_anonymous):
		if(user.is_first_login):
			data = data_to_json(True)
			return JsonResponse(data,safe=False)  
		else:
			if(user.telegramid and user.email):
				data = data_to_json(False)
				return JsonResponse(data,safe=False)
			else:
				data = data_to_json(True)
				return JsonResponse(data,safe=False)
	else:
		data = data_to_json(False)
		return JsonResponse(data,safe=False)

def data_to_json(bool):
	data = {"bool":bool}
	return data

def get_first_login(request):
	if request.method == "POST":
		email = request.POST.get('email')
		tgid = request.POST.get('tgid')
		if(email and tgid):
			User.objects.filter(id=request.user.id).update(telegramid=tgid,email=email,is_first_login=False)
			return JsonResponse({"bool": True}, status=200)
		else:
			print('false')
			return JsonResponse({"bool": False}, status=200)
	else:
		errors = 'error'
		print(errors)
		return JsonResponse({"errors": errors}, status=400)

