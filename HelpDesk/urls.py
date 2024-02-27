from django.contrib import admin
from django.urls import path, include
from task.views import *

urlpatterns = [
    path('', admin.site.urls),
    path('task/list/<slug:tgid>/', get_list_task_for_tg_user, name='get_list_task_for_tg_user'),

]
