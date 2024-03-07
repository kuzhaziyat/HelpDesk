from django.contrib import admin
from django.urls import path, include
from task.views import *

urlpatterns = [
    path('', admin.site.urls),
    path('task/get_departments/<int:org_id>/', get_department, name='get_department'),
]
