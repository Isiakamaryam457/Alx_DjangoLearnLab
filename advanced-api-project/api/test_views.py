from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):

    def setUp(self):
        """
        Set up test data before each test runs.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.author = Author.objects.create(name="Chinua Achebe")

        self.book = Book.objects.create(
            title="Things Fall Apart",
            publication_year=1958,
            author=self.author
        )

        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book.id}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/{self.book.id}/update/"
        self.delete_url = f"/api/books/{self.book.id}/delete/"

    # -----------------------------
    # READ TESTS
    # -----------------------------

    def test_list_books(self):
        """
        Test retrieving list of books.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_book(self):
        """
        Test retrieving a single book by ID.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    # -----------------------------
    # CREATE TESTS
    # -----------------------------

    def test_create_book_authenticated(self):
        """
        Authenticated users can create a book.
        """
        self.client.login(username="testuser", password="testpassword")

        data = {
            "title": "No Longer at Ease",
            "publication_year": 1960,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        """
        Unauthenticated users cannot create a book.
        """
        data = {
            "title": "Arrow of God",
            "publication_year": 1964,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -----------------------------
    # UPDATE TESTS
    # -----------------------------

    def test_update_book_authenticated(self):
        """
        Authenticated users can update a book.
        """
        self.client.login(username="testuser", password="testpassword")

        data = {
            "title": "Things Fall Apart (Updated)",
            "publication_year": 1958,
            "author": self.author.id
        }

        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------------
    # DELETE TESTS
    # -----------------------------

    def test_delete_book_authenticated(self):
        """
        Authenticated users can delete a book.
        """
        self.client.login(username="testuser", password="testpassword")

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # -----------------------------
    # SEARCH & ORDERING TESTS
    # -----------------------------

    def test_search_books(self):
        """
        Test search functionality.
        """
        response = self.client.get(self.list_url + "?search=Things")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_books_by_year(self):
        """
        Test ordering functionality.
        """
        response = self.client.get(self.list_url + "?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
