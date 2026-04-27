from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Admin User Management (Day 9)
    path('admin/users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin/users/add/', views.admin_add_user, name='admin_add_user'),
    path('admin/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/users/upload_csv/', views.upload_users_csv, name='upload_users_csv'),
]