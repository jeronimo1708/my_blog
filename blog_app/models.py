# blog_app/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # For get_absolute_url
from taggit.managers import TaggableManager # For tags

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # New field for likes
    likers = models.ManyToManyField(User, related_name='liked_posts', blank=True) # Users who liked this post

    # New field for tags
    tags = TaggableManager() # Provides a manager to add, retrieve, and remove tags from Post objects

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # Link to the Post
    name = models.CharField(max_length=80) # Commenter's name
    email = models.EmailField() # Commenter's email
    body = models.TextField() # Comment body
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # For moderation: only active comments are displayed

    class Meta:
        ordering = ('created',) # Order comments by creation date

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'