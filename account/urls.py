from django.urls import path

from . import views


app_name = 'account'
urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),

    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.user_logout_view, name='user_logout'),

    path('<username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('<username>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('<username>/update/', views.UserUpdateProfileView.as_view(), name='user_update'),
    path('<username>/posts/', views.UserPostsView.as_view(), name='user_posts'),
    path('<username>/follow/', views.UserFollowView.as_view(), name='user_follow'),
    path('<username>/unfollow/', views.UserUnfollowView.as_view(), name='user_unfollow'),

    path('<username>/followers/', views.user_followers_view, name='user_followers'),
    path('<username>/followings/', views.user_followings_view, name='user_followings'),

    path('<username>/create-music/', views.UserMusicCreateView.as_view(), name='user_create_music'),
    path('<str:username>/musics/<int:id>/delete/', views.user_music_delete_view, name='user_music_delete'),
    path('<username>/musics/', views.user_musics_view, name='user_musics'),

    path('<username>/create-image/', views.UserImageCreateView.as_view(), name='user_create_image'),
    path('<str:username>/images/<int:id>/delete/', views.user_image_delete_view, name='user_image_delete'),
    path('<username>/images/', views.user_images_view, name='user_images')
]
