from django.db.models import Model, CharField, SlugField, TextField, DateTimeField, Index, URLField, ForeignKey, BooleanField, EmailField
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


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
    slug = SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post')
    body = TextField()
    publish = DateTimeField(default=timezone.now)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    status = CharField(max_length=2, choices=Status, default=Status.DRAFT)

    cover_img = URLField(blank=True, null=True,
                         default='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Altja_j%C3%B5gi_Lahemaal.jpg/1920px-Altja_j%C3%B5gi_Lahemaal.jpg'
                         )
    img_description = TextField(blank=True, null=True, default='Forest with a river')

    objects = models.Manager() # Default manager
    published = PublishedManager() # Our custom manager

    class Meta:
        ordering = ['-publish']
        indexes = [Index(fields=['-publish']),]


    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Post: {self.title}>"

    def get_absolute_url(self):
        return reverse(
            'blog:detail',
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug]
        )


class Comment(Model):
    post = ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = CharField(max_length=80)
    email = EmailField()
    body = TextField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    active = BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [Index(fields=['created']),]

        def __str__(self):
            return f"Comment by {self.name} on {self.post}"
