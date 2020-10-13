from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from grade.models import Grade


class Classroom(models.Model):
    """A school classroom"""

    def validate_comma_separated_weekday_list(comma_sep_string):
        for day_str in comma_sep_string.split(','):
            try:
                day = int(day_str)
            except ValueError:
                raise ValidationError(_(
                    "Days of the week must be a comma separated integer list"
                ))
            else:
                if day < 1 or day > 7:
                    raise ValidationError(_(
                        "Days of the week must be between 1 and 7"
                    ))

    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=50, unique=True)
    room = models.CharField(max_length=50)
    days_of_week = models.CharField(
        max_length=30,
        validators=[
            validate_comma_separated_integer_list,
            validate_comma_separated_weekday_list
        ]
    )
    time = models.TimeField()
    grade = models.ForeignKey(
        Grade,
        null=True,
        on_delete=models.SET_NULL,
        related_name='classes'
    )

    def __str__(self):
        """String represetation of the model"""
        return self.identifier + ' - ' + self.name
