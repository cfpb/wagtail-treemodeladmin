from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Volume(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
