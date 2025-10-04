from django.db import models


class Book(models.Model):
    name = models.CharField(
        verbose_name="Название",
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    year = models.PositiveIntegerField(
        verbose_name="Год издания",
    )

    genre = models.ForeignKey(
        "Genre",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        "Author",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name="Название",
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        verbose_name="Фамилия",
    )
    patronymic = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name="Отчество",
    )
    date_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата рождения",
    )
    date_death = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата смерти",
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Биография",
    )

    def __str__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."
