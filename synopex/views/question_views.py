from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Question, Answer, Comment, Board
from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="common:login")
def question_create(request, board_name):
    board = get_object_or_404(Board, name=board_name)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.board = board  # Set the board here
            question.save()
            return redirect("synopex:board_filtered", board_name=board.name)
    else:
        form = QuestionForm()
    context = {"form": form, "board": board}
    return render(request, 'synopex/question_form.html', context)

@login_required(login_url="common:login")
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("synopex:detail", question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect("synopex:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {"form":form}
    return render(request, "synopex/question_form.html", context)

@login_required(login_url="common:login")
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제권한이 없습니다")
        return redirect("synopex:detail", question_id=question.id)
    board_name = question.board.name if question.board else None
    question.delete()
    return redirect("synopex:board_filtered", board_name=board_name)
