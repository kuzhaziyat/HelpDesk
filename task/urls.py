from django.urls import path
from .views import *

urlpatterns = [
    path('getexecutor/<int:dep_id>/', get_executor, name='get_executor'),
    path('getdepartments/<int:org_id>/', get_department, name='get_department'),
]