from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the conversion of Book model instances to/from JSON.
    It includes all fields from the Book model and implements custom validation
    for the publication_year field.
    
    Fields:
        id: Auto-generated primary key
        title: Book title
        publication_year: Year of publication (validated to not be in future)
        author: Foreign key ID linking to the Author
    
    Validation:
        - Ensures publication_year is not in the future using custom validator
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not set to a future year.
        This prevents data entry errors and maintains data integrity.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer handles the conversion of Author model instances to/from JSON.
    It demonstrates a nested relationship by including all related books for each
    author through the BookSerializer.
    
    Fields:
        id: Auto-generated primary key
        name: Author's full name
        books: Nested list of all books written by this author (read-only)
    
    Nested Serialization:
        The 'books' field uses BookSerializer to serialize all related Book objects.
        - many=True: Indicates this is a list of books (one-to-many relationship)
        - read_only=True: Books are only shown in GET requests, not required for POST
        
    Relationship Handling:
        The relationship between Author and Book is handled through:
        1. The 'books' field in this serializer uses the related_name='books' 
           defined in the Book model's ForeignKey
        2. Django ORM automatically populates this field with all books 
           where author_id matches this Author's id
        3. BookSerializer is used to serialize each related book, providing
           full book details (title, publication_year, etc.) nested within
           the author's JSON response
        
    Example JSON output:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Harry Potter and the Chamber of Secrets",
                    "publication_year": 1998,
                    "author": 1
                }
            ]
        }
    """
    
    # Nested serializer to include all related books for this author
    # Uses the reverse relation 'books' from the ForeignKey's related_name
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']