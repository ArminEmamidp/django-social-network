from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'created', 'updated']
    list_filter = ['title', 'user', 'created']
    search_fields = ['id', 'user', 'title', 'created']
    prepopulated_fields = {'slug':['description']}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'is_reply', 'created']
    list_filter = ['user', 'post', 'is_reply']
    list_editable = ['is_reply']
    search_fields = ['id', 'user', 'post', 'created']