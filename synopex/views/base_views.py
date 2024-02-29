from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Question, Answer, Comment, Board
from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

def index(request, board_name="free_board"):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get("so", "recent")

    # Initialize the query for all questions or filter by board if board_name is given
    if board_name:
        board = get_object_or_404(Board, name=board_name)
        question_list = Question.objects.filter(board=board)
    else:
        board = None
        question_list = Question.objects.all()

    # Apply filtering based on 'so' and 'kw'
    if so == "recommend":
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == "popular":
        question_list = question_list.annotate(num_answer=Count("answer")).order_by("-num_answer", "-create_date")
    else:
        question_list = question_list.order_by("-create_date")

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    
    print(board)
    context = {
        "board": board,  # Include the board in context
        "question_list": page_obj,
        'page': page,
        'kw': kw,
        'so': so
    }
    return render(request, 'synopex/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, 'synopex/question_detail.html', context)

