from django.contrib.auth import get_user_model
from django.db import models

from apps.base.TimeStampModel import TimeStampModel


class Category(TimeStampModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name