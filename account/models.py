from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    
    def __str__(self):
        return self.user.username


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.from_user.username} followed {self.to_user.username}"


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    body = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def delete(self):
        return reverse('account:user_story_delete', args=[self.user.username, self.pk])


class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='musics')
    singer_name = models.CharField(max_length=50)
    song_name = models.CharField(max_length=100)
    music = models.FileField(upload_to='musics/users/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.singer_name} - {self.song_name}"
    
    def delete(self):
        return reverse('account:user_delete_music', args=[self.user.username, self.pk])