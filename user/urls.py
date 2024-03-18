from django.urls import path
from .views import *
urlpatterns = [
	path('is_first_login/', is_first_login, name='is_first_login'),
    path('postDataFL/',get_first_login,name='get_first_login')
]