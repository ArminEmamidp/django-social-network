from django.contrib import admin

from .models import Relation, Music, Image


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'created']
    list_filter = ['from_user', 'to_user', 'created']


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'auther', 'singer_name', 'music_name', 'created']
    list_display = ['auther', 'singer_name', 'music_name', 'created']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'auther', 'created']
    list_filter = ['id', 'auther', 'created']
