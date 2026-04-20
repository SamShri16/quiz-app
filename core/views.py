from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Quiz, Question, Option
from django.contrib.auth.decorators import login_required


# ---------------- HOME ----------------
def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})


# ---------------- CATEGORY QUIZZES ----------------
def category_quizzes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = category.quiz_set.all()
    return render(request, 'core/quizzes_by_category.html', {
        'category': category,
        'quizzes': quizzes
    })


# ---------------- START QUIZ ----------------
@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    request.session['quiz_id'] = quiz_id
    request.session['question_index'] = 0
    request.session['score'] = 0
    request.session['answers'] = {}

    return redirect('attempt_quiz')


# ---------------- ATTEMPT QUIZ ----------------
@login_required
def attempt_quiz(request):
    quiz_id = request.session.get('quiz_id')
    question_index = request.session.get('question_index', 0)

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = list(quiz.question_set.all())

    if question_index >= len(questions):
        return redirect('quiz_result')

    current_question = questions[question_index]
    options = current_question.options.all()

    if request.method == 'POST':
        selected_option_id = request.POST.get('option')

        if selected_option_id:
            selected_option = Option.objects.get(id=selected_option_id)

            answers = request.session.get('answers', {})
            answers[str(current_question.id)] = selected_option.id
            request.session['answers'] = answers

            if selected_option.is_correct:
                request.session['score'] = request.session.get('score', 0) + 1

        request.session['question_index'] = question_index + 1
        return redirect('attempt_quiz')

    return render(request, 'core/quiz_attempt.html', {
        'question': current_question,
        'options': options,
        'question_number': question_index + 1,
        'total_questions': len(questions),
    })


# ---------------- RESULT ----------------
@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('quiz_id')

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    total_questions = quiz.question_set.count()

    context = {
        'score': score,
        'total_questions': total_questions,
        'quiz': quiz,
    }

    # Clear session
    for key in ['score', 'quiz_id', 'question_index', 'answers']:
        request.session.pop(key, None)

    return render(request, 'core/quiz_result.html', context)