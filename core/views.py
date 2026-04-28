from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Category, Quiz, Question, Option, Attempt, Answer

import csv
from io import TextIOWrapper


# ✅ HOME VIEW (YOU WERE MISSING THIS)
def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})


# ================= AUTH =================

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully.")
        return redirect('login')

    return render(request, 'core/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ================= QUIZ =================

def category_quizzes(request, category_id):
    quizzes = Quiz.objects.filter(category_id=category_id)
    return render(request, 'core/quizzes_by_category.html', {'quizzes': quizzes})


@login_required
def start_quiz(request, quiz_id):
    request.session['quiz_id'] = quiz_id
    request.session['question_index'] = 0
    request.session['score'] = 0
    request.session['answers'] = {}
    return redirect('attempt_quiz')


@login_required
def attempt_quiz(request):
    quiz_id = request.session.get('quiz_id')
    question_index = request.session.get('question_index', 0)

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    if question_index >= len(questions):
        return redirect('quiz_result')

    question = questions[question_index]
    options = question.options.all()

    if request.method == 'POST':
        selected = request.POST.get('option')

        if selected:
            option = Option.objects.get(id=selected)
            request.session['answers'][str(question.id)] = option.id

            if option.is_correct:
                request.session['score'] += 1

        request.session['question_index'] += 1
        return redirect('attempt_quiz')

    return render(request, 'core/quiz_attempt.html', {
        'question': question,
        'options': options,
        'question_number': question_index + 1,
        'total_questions': len(questions)
    })


@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('quiz_id')
    answers = request.session.get('answers', {})

    quiz = get_object_or_404(Quiz, id=quiz_id)
    total = quiz.question_set.count()

    attempt = Attempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total=total
    )

    for qid, oid in answers.items():
        Answer.objects.create(
            attempt=attempt,
            question_id=qid,
            selected_option_id=oid
        )

    for key in ['score', 'quiz_id', 'question_index', 'answers']:
        request.session.pop(key, None)

    return render(request, 'core/quiz_result.html', {
        'score': score,
        'total_questions': total,
        'quiz': quiz
    })


@login_required
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user)
    return render(request, 'core/my_attempts.html', {'attempts': attempts})


# ================= ADMIN DASHBOARD =================

@staff_member_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')


# ================= USER MANAGEMENT (DAY 9) =================

@staff_member_required
def admin_manage_users(request):
    users = User.objects.all()
    return render(request, 'core/admin_users.html', {'users': users})


@staff_member_required
def admin_add_user(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        return redirect('admin_manage_users')

    return render(request, 'core/admin_add_user.html')


@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()
        return redirect('admin_manage_users')

    return render(request, 'core/admin_edit_user.html', {'user': user})


@staff_member_required
def delete_user(request, user_id):
    get_object_or_404(User, id=user_id).delete()
    return redirect('admin_manage_users')


@staff_member_required
def upload_users_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)

        for row in reader:
            if not User.objects.filter(username=row['username']).exists():
                User.objects.create_user(
                    username=row['username'],
                    email=row['email'],
                    password=row['password']
                )

        return redirect('admin_manage_users')

    return render(request, 'core/admin_upload_users.html')


# ✅ QUIZ MANAGEMENT (needed for your URL)

@staff_member_required
def admin_manage_quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'core/admin_manage_quizzes.html', {'quizzes': quizzes})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        confirm  = request.POST.get('confirm_password')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'core/register.html')



