from django.contrib import admin
from django.urls import path, re_path, include
import task,user
urlpatterns = [
    path('admin/', admin.site.urls),
    path("task/", include("task.urls")),
    path("user/", include("user.urls")),

]
