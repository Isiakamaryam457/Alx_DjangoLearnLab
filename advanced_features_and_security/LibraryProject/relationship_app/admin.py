from django.contrib import admin
from .models import Author, Book, Library, UserProfile
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(UserProfile)