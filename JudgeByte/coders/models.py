from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

from django.urls import reverse


class UserProfile(AbstractUser):
    name = models.CharField(blank=True, max_length=200)
    score = models.PositiveIntegerField(blank=True, null=True, default = 0)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('coders:user_info', kwargs={'username':self.username})

    class Meta:
        permissions = (("can_set_problems", "Required for setting problems"),)

class Faqs(models.Model):
    question = models.TextField(blank = True)
    answer = models.TextField(blank = True)

    def __str__(self):
        return self.question
