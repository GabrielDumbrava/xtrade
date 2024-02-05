""" General models unrelated to specific feature. """
from django.db import models


class Exchange(models.Model):
    """ Exchange model. """
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
