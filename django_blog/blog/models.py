from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Tag(models.Model):
    """
    Tag model for categorizing blog posts.
    A tag can be associated with multiple posts.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to see all posts with this tag."""
        return reverse('posts-by-tag', kwargs={'tag_name': self.name})


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    class Meta:
        ordering = ['-published_date']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the URL to access a detail view for this post."""
        return reverse('post-detail', kwargs={'pk': self.pk})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']  # Oldest comments first
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


