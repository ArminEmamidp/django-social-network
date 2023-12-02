from django.urls import path
from . import views



app_name = 'posts'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    
    path('<post_id>/<post_slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<post_id>/<post_slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    
    path('<post_id>/<post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<post_id>/<post_slug>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('<post_id>/<post_slug>/<comment_id>/', views.AddReplyCommentView.as_view(), name='post_comment_reply'),
    
    path('post-create/', views.PostCreateView.as_view(), name='post_create')
]