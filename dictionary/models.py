from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Word(models.Model):
    text = models.CharField(max_length=50, unique=True)
    url_text = models.CharField(max_length=60, null=True, blank=True)
    definition = models.TextField(max_length=300)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.text
    def clean(self):
        self.url_text = self.text.replace(" ", "-")

class Comment(models.Model):
    text = models.TextField(max_length=300)
    author = models.ForeignKey(User)
    about = models.ForeignKey(Word)
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    def __str__(self):
        return self.text

class Reaction(models.Model):
    user = models.ForeignKey(User)
    word = models.ForeignKey(Word, null=True, blank=True)
    comment = models.ForeignKey(Comment, null=True, blank=True)
    negative = models.BooleanField(default=False)
    def __str__(self):
        if self.word is not None:
            if self.negative:
                return "{0} disliked {1}".format(str(self.user), str(self.word))
            else:
                return "{0} liked {1}".format(str(self.user), str(self.word))
        else:
            if self.negative:
                return "{0} disliked {1}".format(str(self.user), str(self.comment))
            else:
                return "{0} liked {1}".format(str(self.user), str(self.comment))
