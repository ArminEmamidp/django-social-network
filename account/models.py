from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)
    bio = models.TextField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return f"profile of {self.user.username}"


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']

    def __str__(self):
        return f"{self.from_user.username} followed {self.to_user.username}"


class Music(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='musics')
    singer_name = models.CharField(max_length=100)
    music_name = models.CharField(max_length=100)
    music_file = models.FileField(upload_to='users/musics/', validators=[FileExtensionValidator(['mp3', 'wav'])])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']

    def music_delete(self):
        return reverse('account:user_music_delete', args=[self.auther, self.id])

    def __str__(self):
        return f"{self.singer_name} - {self.music_name}"


class Image(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='users/images/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'tif', 'tiff', 'bmp'])])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']

    def __str__(self):
        return f"Image id: {self.id}"

    def image_delete(self):
        return reverse('account:user_image_delete', args=[self.auther, self.id])


class Story(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    content = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def story_delete(self):
        return reverse('account:user_story_delete', args=[self.auther, self.id])


class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    def str(self):
        return f"The links of {self.user.username}"
    
    def link_delete(self):
        return reverse('account:user_link_delete', args=[self.user.username, self.id])
