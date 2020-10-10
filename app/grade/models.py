from django.db import models


class Grade(models.Model):
    """Represents the school level a student is in"""

    name = models.CharField(max_length=100)
    rank = models.PositiveSmallIntegerField()

    def __str__(self):
        """Return a string representation of the Grade model"""
        return self.name
