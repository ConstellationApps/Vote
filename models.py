from django.db import models
from json import JSONEncoder

class Candidate(models.Model):
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=512, null=True)

    def __str__(self):
        return self.name

class Vote(models.Model):
    uid = models.CharField(max_length=75)
    order = models.CharField(max_length=128)
    timestamp = models.DateTimeField('Date Cast')

    def __str__(self):
        return "Vote from " + self.uid
