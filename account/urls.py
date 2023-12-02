from django.urls import path
from . import views



app_name = 'account'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),

    path('create-story/', views.UserCreateStoryView.as_view(), name='user_create_story'),
    path('create-music/', views.UserCreateMusicView.as_view(), name='user_create_music'),
    path('user-list/', views.FindFriendsView.as_view(), name='user_list'),
    
    path('<username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('<username>/follow/', views.UserFollowView.as_view(), name='user_follow'),
    path('<username>/unfollow/', views.UserUnfollowView.as_view(), name='user_unfollow'),
    path('<username>/edit-profile/', views.UserEditProfileeView.as_view(), name='user_edit_profile'),

    path('<username>/musics/<music_id>/delete/', views.UserDeleteMusicView.as_view(), name='user_delete_music'),
    path('<username>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('<username>/stories/<story_id>/delete/', views.UserDeleteStoryView.as_view(), name='user_story_delete'),

    path('<username>/posts/', views.UserPostsView.as_view(), name='user_posts'),
    path('<username>/followers/', views.UserFollowersView.as_view(), name='user_followers'),
    path('<username>/followings/', views.UserFollowingsView.as_view(), name='user_followings'),
    path('<username>/stories/', views.UserStoriesView.as_view(), name='user_stories'),
    path('<username>/musics/', views.UserMusicsView.as_view(), name='user_musics'),
]
