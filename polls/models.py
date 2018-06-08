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
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)

    def _votes(self):
        return self.vote_set.count()
    votes = property(_votes)

    def num_votes_by_user(self, user):
        try:
            return self.vote_set.filter(user=user).count()
        except (Vote.DoesNotExist):
            return 0

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

def vote(self, choice):
    return Vote.objects.create(
        user=(self if type(self) is User else None),
        choice=choice
    )

User.add_to_class("vote", vote)
AnonymousUser.vote = vote
