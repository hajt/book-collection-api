from typing import Any
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator
)


class AuthorManager(models.Manager):
    """ Author custom manager class. """

    def get_or_create_from_str(self, author: str) -> Any:
        """ Method which gets or creates (if doesn't exists) author object
        from passed author in string format. """
        author = author.split()
        first_name = author[0]
        second_name = ' '.join(author[1:-1])
        last_name = author[-1]
        obj, created = self.get_or_create(
            first_name=first_name, last_name=last_name)
        if second_name and created:
            obj.second_name = second_name
            obj.save()
        return obj


class Author(models.Model):
    """ Author model class. """
    objects = AuthorManager()
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'first_name',
                    'last_name'],
                name='unique_author')]

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.last_name}" if self.second_name else f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Author(first_name='{self.first_name}', second_name='{self.second_name}', last_name='{self.last_name}')>"


class Category(models.Model):
    """ Category model class. """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Category(name='{self.name}')>"


class Book(models.Model):
    """ Books model class. """
    title = models.CharField(max_length=150)
    isbn = models.PositiveIntegerField(
        unique=True, validators=[MinLengthValidator(13), MaxLengthValidator(13)])

    category = models.ForeignKey(
        Category, related_name='books', on_delete=models.PROTECT)
    author = models.ForeignKey(
        Author, related_name='books', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title}, ISBN: {self.isbn}"

    def __repr__(self):
        return f"<Book(title='{self.title}', isbn={self.isbn}')>"


class Opinion(models.Model):
    """ Opinion model class. """
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=500)

    book = models.ForeignKey(
        Book, related_name='opinions', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.rate}, '{self.description}'"

    def __repr__(self):
        return f"<Opinion(rate='{self.rate}', description={self.description}')>"
