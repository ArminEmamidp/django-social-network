from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from froala_editor.fields import FroalaField


class Post(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=500)
    description = models.TextField()
    # body = models.TextField()
    # image = models.ImageField(upload_to='posts/images/')
    body = FroalaField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def post_detail(self):
        return reverse('base:post_detail', args=[self.pk])

    def post_delete(self):
        return reverse('base:post_delete', args=[self.pk])

    def post_like(self):
        return reverse('base:post_like', args=[self.pk])

    def post_update(self):
        return reverse('base:post_update', args=[self.pk])


class Comment(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.auther} posted a comment to: {self.post.title}"
    
    def comment_delete(self):
        return reverse('base:post_comment_delete', args=[self.post.pk, self.pk])


class Like(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auther} liked post: {self.post.title}"

