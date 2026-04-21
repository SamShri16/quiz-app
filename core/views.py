from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Option, Attempt, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})




def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'core/home.html', {'quizzes': quizzes})


@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    request.session['quiz_id'] = quiz.id
    request.session['question_index'] = 0
    request.session['score'] = 0
    request.session['answers'] = {}

    return redirect('quiz_question')


@login_required
def quiz_question(request):
    quiz_id = request.session.get('quiz_id')
    question_index = request.session.get('question_index', 0)

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = list(quiz.question_set.all())

    if question_index >= len(questions):
        return redirect('quiz_result')

    question = questions[question_index]

    if request.method == 'POST':
        selected_option_id = request.POST.get('option')
        option = Option.objects.get(pk=selected_option_id)

        answers = request.session.get('answers', {})
        answers[str(question.id)] = selected_option_id
        request.session['answers'] = answers

        if option.is_correct:
            request.session['score'] += 1

        request.session['question_index'] += 1
        return redirect('quiz_question')

    return render(request, 'core/quiz_question.html', {
        'question': question
    })


@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('quiz_id')

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    total_questions = quiz.question_set.count()
    answers = request.session.get('answers', {})

    # Save Attempt
    attempt = Attempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total=total_questions,
    )

    # Save Answers
    for qid, oid in answers.items():
        question = Question.objects.get(pk=qid)
        option = Option.objects.get(pk=oid)

        Answer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=option
        )

    # Clear session
    for key in ['score', 'quiz_id', 'question_index', 'answers']:
        request.session.pop(key, None)

    return render(request, 'core/quiz_result.html', {
        'score': score,
        'total_questions': total_questions,
        'quiz': quiz
    })


@login_required
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'core/my_attempts.html', {
        'attempts': attempts
    })

