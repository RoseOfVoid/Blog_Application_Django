from django.db.models import Model, CharField, SlugField, TextField, DateTimeField, Index
from django.db import models
from django.utils import timezone
from django.conf import settings


class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = CharField(max_length=250)
    slug = SlugField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post')
    body = TextField()
    publish = DateTimeField(default=timezone.now)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    status = CharField(max_length=2, choices=Status, default=Status.DRAFT)

    objects = models.Manager() # Default manager
    published = PublishedManager() # Our custom manager

    class Meta:
        ordering = ['-publish']
        indexes = [Index(fields=['-publish']),]


    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Post: {self.title}>"
