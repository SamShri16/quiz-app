from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_manage_quizzes/', views.admin_manage_quizzes, name='admin_manage_quizzes'),

]