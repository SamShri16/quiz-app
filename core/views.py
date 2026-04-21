from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.contrib.auth.models import User

from .models import Quiz, Attempt


# ✅ HOME (FIXES YOUR CRASH)
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'home.html', {'quizzes': quizzes})


# ✅ MY ATTEMPTS
@login_required
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_attempts.html', {'attempts': attempts})


# ✅ ADMIN DASHBOARD
@staff_member_required
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_quizzes': Quiz.objects.count(),
        'total_attempts': Attempt.objects.count(),
        'top_quizzes': Quiz.objects.annotate(
            attempts_count=Count('attempt')
        ).order_by('-attempts_count')[:5],
    }

    return render(request, 'admin_dashboard.html', context)