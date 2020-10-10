from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from grade.models import Grade


class Class(models.Model):
    """A school class"""

    def validate_comma_separated_weekday_list(comma_sep_string):
        for stringed_num in comma_sep_string.split(','):
            if not (1 <= int(stringed_num) <= 7):
                raise ValidationError(_("Invalid day of the week!"))

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
