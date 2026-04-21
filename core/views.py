from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Attempt, Answer


def home(request):
    categories = []
    return render(request, 'core/home.html', {'categories': categories})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})

@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('quiz_id')
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    total_question = quiz.question_set_count()
    answers = request.session.get('answers', {})

    # Save attempt
    attempt = Attempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total=total_question
    )

    # Save each answer 
    for qid, oid in answers.items():
        questions = Question.objects.get(pk=qid)
        option = Opton.objects.get(pk=oid)
        Answer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=option
        )

    # Clear session 
    for key in['score','quiz_id','question_index','asnwers']:
        request.session.pop(key, None)

    return.render(request, 'core/quiz_result.html' , {
        'score': score,
        'total_questions' : total_question
        'quiz': quiz

    })


@login_required
def my_ateempts(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'core/my_attempts.html', {'attempts': attempts})