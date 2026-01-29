from django.db import models

class Book(models.Model):
    title = models.Charfield(max_length=200)
    author = models.Charfield(max_length=100)
