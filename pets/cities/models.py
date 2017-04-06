from django.db import models


class State(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=2)


class City(models.Model):
    state = models.ForeignKey(State)
    code = models.IntegerField()
    name = models.CharField(max_length=80)
    search_name = models.CharField(max_length=80)
