from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Quiz, Attempt


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