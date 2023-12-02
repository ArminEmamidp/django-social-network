from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    description = models.TextField(max_length=500)
    main_image = models.ImageField(upload_to='images/posts/')
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("posts:post_detail", args=[self.pk, self.slug])
    
    def post_like(self):
        return reverse("posts:post_like", args=[self.pk, self.slug])
    
    def post_delete(self):
        return reverse("posts:post_delete", args=[self.pk, self.slug])
    
    def post_update(self):
        return reverse("posts:post_update", args=[self.pk, self.slug])
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user.username} liked the {self.post.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    body = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.user.username} senf a comment to the {self.post.title}"

    def add_reply(self):
        return reverse('posts:post_comment_reply', args=[self.post.pk, self.post.slug, self.pk])
    