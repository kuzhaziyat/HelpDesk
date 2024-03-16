from django.contrib import admin
from django.urls import path, re_path, include
import task
urlpatterns = [
    path('admin/', admin.site.urls),
    path("task/", include("task.urls")),
]
