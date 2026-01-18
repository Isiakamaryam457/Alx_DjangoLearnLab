from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

def list_books(request):
    book = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'books/book_list.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    