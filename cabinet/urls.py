from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cabinet'

urlpatterns = [
	path('', views.cabinet, name='cabinet'),
	path('add/<int:book_id>/', views.addbook, name='addbook'),
	path('registration/', views.reg, name='reg'),
	path('login/', views.log, name='login'),
	path('logout/', views.user_logout, name='logout'),
]