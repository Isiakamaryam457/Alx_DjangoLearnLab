from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView,
    CommentCreateView, 
    CommentUpdateView,
    CommentDeleteView,
    PostSearchView,   # Add this
    PostByTagView,    # Add this
)


urlpatterns = [
   
    # Blog post URLs
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Search URLs
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),


    # Comment URLs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add-comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    

    # Authentication url patterns
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html',  http_method_names=['get', 'post']), name='logout'),
]