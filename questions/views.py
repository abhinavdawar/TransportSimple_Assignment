from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def home(request):
    questions = Question.objects.all()
    return render(request, 'questions/home.html', {'questions': questions})


@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'questions/post_question.html', {'form': form})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=question.pk)
    else:
        answer_form = AnswerForm()

    return render(request, 'questions/question_detail.html', {
        'question': question,
        'answers': answers,
        'answer_form': answer_form
    })


@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)
    if not created:
        like.delete()  # Unlike if already liked
    return redirect('question_detail', pk=answer.question.pk)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect to login page after successful sign up
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def post_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = AnswerForm()

    return render(request, 'questions/question_detail.html', {
        'question': question,
        'answers': question.answers.all(),
        'form': form
    })

