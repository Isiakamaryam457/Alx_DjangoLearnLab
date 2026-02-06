from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores basic information about authors and establishes
    a one-to-many relationship with the Book model (one author can have
    multiple books).
    
    Fields:
        name (CharField): The full name of the author, max 200 characters.
    
    Relationships:
        books: Reverse relation to Book model via ForeignKey.
               Accessible using author.books.all()
    """
    name = models.CharField(max_length=200)
    
    def __str__(self):
        """String representation of the Author object."""
        return self.name
    
    class Meta:
        ordering = ['name']  # Default ordering by name alphabetically


class Book(models.Model):
    """
    Book model representing a published book.
    
    This model stores information about books and links each book to
    an author through a ForeignKey relationship.
    
    Fields:
        title (CharField): The title of the book, max 200 characters.
        publication_year (IntegerField): The year the book was published.
        author (ForeignKey): Link to the Author model establishing the
                             one-to-many relationship (many books to one author).
    
    Relationships:
        author: ForeignKey to Author model with CASCADE delete behavior.
                When an author is deleted, all their books are also deleted.
                Uses related_name='books' for reverse lookups from Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # Delete books when author is deleted
        related_name='books'  # Allows author.books.all() reverse lookup
    )
    
    def __str__(self):
        """String representation showing book title."""
        return self.title
    
    class Meta:
        ordering = ['title']  # Default ordering by title alphabetically