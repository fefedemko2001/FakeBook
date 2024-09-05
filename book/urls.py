from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    about,
    like_post,
    dislike_post,
    add_comment_to_post,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name = 'book-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('about', about, name = 'book-about'),
    path('post/<int:pk>/like/', like_post, name='post-like'),
    path('post/<int:pk>/dislike/', dislike_post, name='post-dislike'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='add-comment'),
]


