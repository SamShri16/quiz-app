from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('category/<int:category_id>/', views.category_quizzes, name='category_quizzes'),

    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/attempt/', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/result/', views.quiz_result, name='quiz_result'),

    path('my-attempts/', views.my_attempts, name='my_attempts'),
]