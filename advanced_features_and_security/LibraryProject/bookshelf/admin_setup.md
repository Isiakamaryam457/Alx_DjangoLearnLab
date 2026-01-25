# Django Admin Configuration for Book Model

## Admin Registration

File: `bookshelf/admin.py`
```python
from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)
```

## Features Implemented:

1. **List Display**: Shows title, author, and publication year in admin list view
2. **Filtering**: Added filters for author and publication year in sidebar
3. **Search**: Enabled search functionality for title and author fields

## Accessing the Admin Interface:

1. Create superuser: `python3 manage.py createsuperuser`
2. Start server: `python3 manage.py runserver`
3. Navigate to: `http://127.0.0.1:8000/admin/`
4. Login with superuser credentials