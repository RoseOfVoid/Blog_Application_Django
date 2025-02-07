from django.db.models import Model, CharField, SlugField, TextField, DateTimeField, Index
from django.forms import models
from django.utils import timezone

class Post(Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = CharField(max_length=250)
    slug = SlugField(max_length=250)
    body = TextField()
    publish = DateTimeField(default=timezone.now)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    status = CharField(max_length=2, choices=Status, default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [Index(fields=['-publish']),]


    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Post: {self.title}>"