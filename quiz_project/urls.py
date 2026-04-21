from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # core app
    path('', include('core.urls')),

    # auth
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', core_views.register, name='register'),
    
    path('my-attempts/', views.my_attempts, name='my_attempts'),
    path('result/', views.quiz_result, name='quiz_result'),



]