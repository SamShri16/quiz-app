from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Category, Quiz, Question, Option, Attempt, Answer


def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username exists")
            return redirect('register')

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        messages.success(request, "Account created")
        return redirect('login')

    return render(request, 'core/register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login")
            return redirect('login')

    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


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
    index = request.session.get('question_index', 0)

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = list(quiz.question_set.all())

    if index >= len(questions):
        return redirect('quiz_result')

    question = questions[index]

    if request.method == 'POST':
        option_id = request.POST.get('option')

        if option_id:
            option = Option.objects.get(id=option_id)

            if option.is_correct:
                request.session['score'] += 1

        request.session['question_index'] += 1
        return redirect('attempt_quiz')

    return render(request, 'core/quiz_attempt.html', {
        'question': question,
        'options': question.options.all(),
        'question_number': index + 1,
        'total_questions': len(questions)
    })


@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('quiz_id')

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    total = quiz.question_set.count()

    Attempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total=total
    )

    request.session.flush()

    return render(request, 'core/quiz_result.html', {
        'score': score,
        'total_questions': total,
        'quiz': quiz
    })


@login_required
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user)
    return render(request, 'core/my_attempts.html', {'attempts': attempts})