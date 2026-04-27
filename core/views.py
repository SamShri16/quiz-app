from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import csv
from io import TextIOWrapper


@staff_member_required
def admin_manage_users(request):
    users = User.objects.all()
    return render(request, 'core/admin_users.html', {'users': users})


@staff_member_required
def admin_add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "User created successfully.")

        return redirect('admin_manage_users')

    return render(request, 'core/admin_add_user.html')


@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('admin_manage_users')

    return render(request, 'core/admin_edit_user.html', {'user': user})


@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('admin_manage_users')


@staff_member_required
def upload_users_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            messages.error(request, "No file uploaded.")
            return redirect('upload_users_csv')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "File is not CSV.")
            return redirect('upload_users_csv')

        file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)

        count = 0

        for row in reader:
            username = row.get('username')
            email = row.get('email')
            password = row.get('password')

            if username and not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password)
                count += 1

        messages.success(request, f"{count} users uploaded successfully.")
        return redirect('admin_manage_users')

    return render(request, 'core/admin_upload_users.html')