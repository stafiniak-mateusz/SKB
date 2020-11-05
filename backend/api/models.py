from django.db import models
from datetime import datetime, timedelta


class Tag(models.Model):
    name = models.CharField(name='name', default='', max_length=256)

    def __str__(self):
        return f'{self.name}'


class News(models.Model):
    title = models.CharField(name='title', default='', max_length=256)
    summary = models.TextField(name='summary', default='')
    source = models.CharField(name='source', default='', max_length=256)
    href = models.CharField(name='href', default='', max_length=256)
    tags = models.ManyToManyField(Tag, blank=True, related_name='news')
    date = models.DateTimeField(default=datetime.now()-timedelta(weeks=3))

    def __str__(self):
        return f'{self.title}, {self.source}'

    class Meta:
        ordering = ['-date']
