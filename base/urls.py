from django.urls import path

from . import views

app_name = 'base'
urlpatterns = [
    path('', views.home_view, name='home'),

    path('posts/', views.PostsView.as_view(), name='posts'),
    path('post-create/', views.PostCreateView.as_view(), name='post_create'),

    path('posts/<id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<id>/delete/', views.post_delete_view, name='post_delete'),
    path('posts/<id>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('posts/<id>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<id>/<comment_id>/', views.post_comment_delete, name='post_comment_delete')
]
