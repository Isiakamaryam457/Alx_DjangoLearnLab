from django.contrib import admin
from .models import Post, Comment, Tag  # Add Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'updated_at')
    list_filter = ('published_date', 'author', 'tags')  # Add tags filter
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)  # Nice widget for managing tags


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
