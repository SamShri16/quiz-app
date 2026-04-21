from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('category/<int:category_id>/', views.quizzes_by_category, name='quizzes_by_category'),

    path('start-quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),

    path('quiz/<int:attempt_id>/', views.take_quiz, name='take_quiz'),

    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('my-attempts/', views.my_attempts, name='my_attempts'),
]