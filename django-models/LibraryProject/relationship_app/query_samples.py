import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

author = Author.objects.get(name="J.K. Rowling")
books_by_author = Book.objects.filter(author=author)
print("Books by", author.name, ":", [book.title for book in books_by_author])

# 2. List all books in a library
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print("Books in", library.name, ":", [book.title for book in books_in_library])

# 3. Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print("Librarian of", library.name, ":", librarian.name)