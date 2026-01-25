# CRUD Operations Documentation

## CREATE Operation

**Command:**
```python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

print(book)
```

**Output:**
```
1984
```

---

## RETRIEVE Operation

**Command:**
```python
from bookshelf.models import Book

# Retrieve the book by title
book = Book.objects.get(title="1984")

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

**Output:**
```
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

---

## UPDATE Operation

**Command:**
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Display the updated book
print(f"Updated title: {book.title}")
```

**Output:**
```
Updated title: Nineteen Eighty-Four
```

---

## DELETE Operation

**Command:**
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

## Summary:

**You need to:**

1. ✅ Create ONE file: `CRUD_operations.md`
2. ✅ Include all 4 operations (Create, Retrieve, Update, Delete)
3. ✅ For each operation, show:
   - The command you ran
   - The output you got
4. ✅ Format it in markdown with code blocks

**File structure:**
```
LibraryProject/
├── bookshelf/
│   └── models.py
├── create.md                    # Individual operation
├── retrieve.md                  # Individual operation
├── update.md                    # Individual operation
├── delete.md                    # Individual operation
└── CRUD_operations.md          # ALL operations combined (this is what you need!)