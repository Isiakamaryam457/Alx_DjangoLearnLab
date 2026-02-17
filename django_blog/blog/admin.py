from django.contrib import admin
from .models import Post, Comment
from taggit.models import Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'updated_at')
    list_filter = ('published_date', 'author') 
    search_fields = ('title', 'content')
   


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
