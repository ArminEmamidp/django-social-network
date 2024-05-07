
from django.contrib import admin

from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'auther', 'title', 'created', 'updated']
    list_filter = ['title', 'auther', 'created', 'updated']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'auther', 'post', 'created']
    list_filter = ['auther', 'post', 'created']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'auther', 'post', 'created']
    list_filter = ['auther', 'post', 'created']
