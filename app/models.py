from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import Subquery, OuterRef, Count

import datetime


class QManager(models.Manager):
    def sortByDate(self):
        aq = Subquery(
            Answer.objects.filter(question_id=OuterRef("pk")).values('question_id').annotate(c=Count("*")).values('c'))
        questions = self.order_by('-date').annotate(answers_count=aq)
        return questions

    def bestQuestions(self):
        aq = Subquery(
            Answer.objects.filter(question_id=OuterRef("pk")).values('question_id').annotate(c=Count("*")).values('c'))
        questions = self.order_by('-ratin').annotate(answers_count=aq)
        return questions

    def questionsByTag(self, tag):
        aq = Subquery(
            Answer.objects.filter(question_id=OuterRef("pk")).values('question_id').annotate(c=Count("*")).values('c'))
        tag_id = Tag.objects.filter(text=tag)[0].id
        questions = self.filter(tags=tag_id).annotate(answers_count=aq)
        return questions

    def answersOnQuestion(self, id):
        return Answer.objects.filter(question_id=id)


class myUManager(UserManager):
    def best(self, n=5):
        return myUser.objects.annotate(active=models.Count('asking')).order_by("-active")[:n]


class TManager(models.Manager):
    def best(self, n=5):
        return Tag.objects.annotate(active=models.Count('tagn')).order_by("-active")[:n]


class myUser(User):
    avatar = models.FileField(upload_to='uploads/', default='IMG_4016.jpg')
    objects = myUManager()


class Tag(models.Model):
    text = models.CharField(max_length=100)
    objects = TManager()


class Question(models.Model):
    asking = models.ForeignKey(myUser, on_delete=models.CASCADE, related_name='asking')
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    ratin = models.IntegerField()
    tags = models.ManyToManyField(Tag, related_name='tagn')
    date = models.DateTimeField(auto_now=True)
    objects = QManager()


class Answer(models.Model):
    answerer = models.ForeignKey(myUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # rating = models.IntegerField()
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class Dislike(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
