import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from .managers import QuestionManager

# Create your models here.

class Question(models.Model):
    objects = QuestionManager()
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    private = models.BooleanField(default=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def num_votes_by_user(self, user):
        return self.vote_set.filter(user=user).count()

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

def vote(self, choice):
    choice.votes += 1
    choice.save()
    return Vote.objects.create(
        user=(self if type(self) is User else None),
        choice=choice
    )

User.add_to_class("vote", vote)
AnonymousUser.vote = vote
