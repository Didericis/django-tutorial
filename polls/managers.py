from django.db import models
from django.utils import timezone

class QuestionManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(pub_date__lte=timezone.now())
