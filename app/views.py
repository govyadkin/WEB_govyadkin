from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator

from app import forms
from app import models

from .models import Question, Answer, myUser, Tag
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from faker import Faker
import random


def paginate(objects_list, request, count_obj):
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1

    paginator = Paginator(objects_list, count_obj)
    if paginator.num_pages == 0:
        return None, None

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except InvalidPage:
        page = paginator.page(1)

    return page.object_list, page


def index(request):
    question_list = Question.objects.sortByDate()

    question_page, page = paginate(question_list, request, 3)
    return render(request, 'index.html', {
        'hot': False,
        'questions': question_page,
        'page': page,
        'best_user': myUser.objects.best(),
        'best_tag': Tag.objects.best(),
    })


def fake(request):
    Answer.objects.all().delete()
    Question.objects.all().delete()
    Tag.objects.all().delete()
    myUser.objects.all().delete()
    faker = Faker()
    t = [Tag(text="Iг"),
         Tag(text="IMGTU"),
         Tag(text="MGTU"),
         Tag(text="MSK"),
         Tag(text="TP"),
         Tag(text="IU")]
    for uu in t:
        uu.save()
    u = [myUser(username=faker.name(), email="f@gmail.com", password="12345678"),
         myUser(username=faker.name(), email="f@gmail.com", password="12345678"),
         myUser(username=faker.name(), email="f@gmail.com", password="12345678"),
         myUser(username=faker.name(), email="f@gmail.com", password="12345678"),
         myUser(username=faker.name(), email="f@gmail.com", password="12345678")]
    for uu in u:
        uu.save()
    for i in range(32):
        q1 = Question(asking=u[random.randint(0, 4)], title=faker.text(100), text=faker.text(500),
                      ratin=random.randint(0, 100))
        q1.save()
        q1.tags.add(t[random.randint(0, 2)])
        q1.tags.add(t[random.randint(3, 5)])
        q1.save()
        for j in range(random.randint(0, 10)):
            a1 = Answer(answerer=u[random.randint(0, 4)], question=q1, text=faker.text(50))
            a1.save()


def login(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'register.html', {})


@login_required
def ask(request):
    return render(request, 'ask.html', {
        'best_user': myUser.objects.best(),
        'best_tag': Tag.objects.best(),
    })


@login_required
def settings(request):
    return render(request, 'settings.html', {})


def hot(request):
    question_list = Question.objects.bestQuestions()
    question_page, page = paginate(question_list, request, 3)
    return render(request, 'index.html', {
        'hot': True,
        'questions': question_page,
        'page': page,
        'best_user': myUser.objects.best(),
        'best_tag': Tag.objects.best(),
    })


def question(request, qid):
    quest = Question.objects.filter(id=qid).first()
    quest.answers_count = Answer.objects.filter(question_id=qid).count()

    answer_list = Question.objects.answersOnQuestion(qid)
    answers_page, page = paginate(answer_list, request, 3)
    return render(request, 'question.html', {
        'question': quest,
        'answers': answers_page,
        'page': page,
        'best_user': myUser.objects.best(),
        'best_tag': Tag.objects.best(),
    })


def tag(request, tag_name):
    question_list = Question.objects.questionsByTag(tag_name)
    question_page, page = paginate(question_list, request, 3)
    return render(request, 'tag.html', {
        'tag': tag_name,
        'questions': question_page,
        'page': page,
        'best_user': myUser.objects.best(),
        'best_tag': Tag.objects.best(),
    })
