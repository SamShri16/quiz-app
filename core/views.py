from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Option, Attempt, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Quiz, Question, Option, Attempt, Answer
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


def quizzes_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = Quiz.objects.filter(category=category)
    return render(request, 'quizzes.html', {'category': category, 'quizzes': quizzes})


@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # create attempt
    attempt = Attempt.objects.create(
        user=request.user,
        quiz=quiz
    )

    return redirect('take_quiz', attempt_id=attempt.id)


@login_required
def take_quiz(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id)
    questions = Question.objects.filter(quiz=attempt.quiz)

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected_option_id = request.POST.get(str(question.id))

            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)

                # save answer
                Answer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=selected_option
                )

                if selected_option.is_correct:
                    score += 1

        # update attempt
        attempt.score = score
        attempt.total = total
        attempt.completed_at = timezone.now()   # ✅ THIS IS THE FIX
        attempt.save()

        return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, 'take_quiz.html', {
        'attempt': attempt,
        'questions': questions
    })


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id)
    return render(request, 'result.html', {'attempt': attempt})


@login_required
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-completed_at')  # ✅ FIXED
    return render(request, 'my_attempts.html', {'attempts': attempts})