from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from api.v1.books.models import Book


class Review(models.Model):
    content = models.TextField(
        blank=True,
        null=True,
    )
    stars = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
