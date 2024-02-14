from django.urls import path
from . import views
urlpatterns = [
	path('', views.home, name='blog-home'),
	path('about/', views.about, name='about-club'),
	path('auth/', views.auth, name='ddd'),
]