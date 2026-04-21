from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('question/', views.quiz_question, name='quiz_question'),
    path('result/', views.quiz_result, name='quiz_result'),

    path('my-attempts/', views.my_attempts, name='my_attempts'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


]