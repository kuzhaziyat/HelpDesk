from django.contrib import admin
from django.urls import path, include
from task.views import *

urlpatterns = [
    path('', admin.site.urls),
    path('task/task/add/sss/change/', get_department, name='get_department'),
]
