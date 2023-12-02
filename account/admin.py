from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Relation, Story, Music


class UserProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInLine]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'created']
	list_filter = ['user', 'created']
	search_fields = ['body']


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'singer_name', 'song_name']
	list_filter = ['user', 'singer_name', 'created']
	search_fields = ['song_name']


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Relation)

