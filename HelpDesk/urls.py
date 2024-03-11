from django.contrib import admin
from django.urls import path, url
from task import urls as taskUrls
urlpatterns = [
    path('', admin.site.urls),
    path('task',taskUrls,name='taskUrls'),
]
