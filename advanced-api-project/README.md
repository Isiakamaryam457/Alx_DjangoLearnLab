# Advanced API Project with Django REST Framework

## Overview

This project demonstrates the development of a Django REST Framework (DRF) API for managing books and authors. It focuses on:

- Using **custom serializers** including nested relationships.
- Implementing **generic class-based views** for CRUD operations.
- Applying **permissions** to protect endpoints.
- Validating data with **custom serializer validation**.

The project is built for learning purposes and uses **SQLite** as the default database.

---

## Project Structure

advanced-api-project/
├── venv/ # Virtual environment
├── manage.py # Django management script
├── db.sqlite3 # SQLite database (after migrations)
├── advanced_api_project/ # Project settings
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
└── api/ # Django app for API
├── init.py
├── admin.py
├── apps.py
├── models.py # Author and Book models
├── serializers.py # Nested serializers
├── views.py # Generic views for CRUD
├── urls.py # URL patterns for API endpoints
└── tests.py