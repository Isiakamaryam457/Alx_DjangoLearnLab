```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
deleted_count = book.delete()

# Confirm deletion by retrieving all books
all_books = Book.objects.all()
print(f"Deleted: {deleted_count}")
print(f"Remaining books: {all_books}")
```

**Output:**
```
Deleted: (1, {'bookshelf.Book': 1})
Remaining books: <QuerySet []>
```
```