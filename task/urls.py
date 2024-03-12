from django.urls import path
from . import views

urlpatterns = [
    path('get_department/<slug:org_id>/', views.get_department, name='get_department'),
]