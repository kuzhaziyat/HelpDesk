from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
	return HttpResponse('<h1>Главная</h1>')
 
def about(request):
	return HttpResponse('<h1>Наш клуб</h1>')
 
@csrf_exempt
def auth(request):
	try:
		flag = request.POST['user_id']
		# TODO use flag
	except KeyError:
		print ('Where is my flag?')
	return HttpResponse('<h1>Авторизация</h1>')