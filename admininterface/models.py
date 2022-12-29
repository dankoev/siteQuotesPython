from django.db import models


class KeysWords(models.Model):
    keyword = models.CharField('Ключевые слова', max_length=50)


class Quotes(models.Model):
    keys = models.ManyToManyField(KeysWords)
    author = models.CharField('Автор', max_length=100)
    content = models.TextField('Содержание')


class Logging(models.Model):
    action = models.TextField('Действие пользователя')
    time = models.DateTimeField()
