from django.contrib.auth.models import User
from django.db import models

import datetime

class QManager(models.Manager):
    def sortByDate(self):
        objects_list = []
        questions = self.order_by('-date')
        for question in questions:
            print(question.asking.avatar.url)
            list_element = question
            list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
            objects_list.append(list_element)
        return objects_list

    def bestQuestions(self):
        objects_list = []
        questions = self.order_by('-ratin')
        for question in questions:
            list_element = question
            list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
            objects_list.append(list_element)
        return objects_list

    def questionsByTag(self, tag):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT question_tags.question_id, tag.text
                    FROM app_question_tags question_tags, app_tag tag
                    WHERE tag.id = question_tags.tag_id AND tag.text = '""" + tag + """'
                    ORDER BY tag.id DESC""")
        objects_list = []
        for row in cursor.fetchall()[:5]:
            question = Question.objects.get(pk=row[0])
            list_element = question
            list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
            objects_list.append(list_element)
        return objects_list

    def answersOnQuestion(self, id):
        return Answer.objects.filter(question_id=id)


class User(models.Model):
    login = models.CharField(max_length=100)
    nick = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    avatar = models.FileField(upload_to='uploads/', default='IMG_4016.jpg')
    date = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    text = models.CharField(max_length=100)


class Question(models.Model):
    asking = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    ratin = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField(auto_now=True)
    objects = QManager()


class Answer(models.Model):
    answerer = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    # rating = models.IntegerField()
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)
