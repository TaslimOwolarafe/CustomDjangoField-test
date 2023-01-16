from django.db import models

from app.fields import CircularCounterField


class State(models.Model):
    counter = CircularCounterField()


