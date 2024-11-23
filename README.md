# Online Bookstore API

The Online Bookstore platform is built using Django and Django Rest Framework (DRF) to create a secure and efficient backend. PostgreSQL is used as the database for managing book, user, and review data, ensuring reliability and performance. The application is containerized with Docker and orchestrated using Docker Compose, enabling seamless deployment and scalability.

----------

## Project Description

The Online Bookstore API enables users to browse, review, and manage books. It provides features such as user registration, book listing, detailed book reviews, and an average rating calculation for books. Built with a focus on scalability, security, and performance, this API adheres to best practices for modern web applications.

----------

## Features

-   **Book Management**:
    -   Add new books via the Django Admin panel.
    -   Add books using custom management commands:
	    -  `add_book` : Use this command to **manually add a book** to the system by providing its details
	    -  `add_fake_books`: Use this command to **quickly generate multiple fake books** with random details
-   **User Functionality**:
    -   Register and log in to the system.
    -   List all available books or view details of a single book.
	-   Create reviews for books.
	-   List all reviews for a specific book (**Add rating and comment**).
-   **Performance & Security**:
    -   Implemented pagination for efficient data handling.
    -   Secured against XSS and SQL Injection using validation and sanitization (via the `bleach` library).
-   **Test Coverage**:
    -   Comprehensive test cases for models, serializers, and views.

----------

## Technologies Used

-   **Django**: Web framework for building the backend.
-   **Django Rest Framework (DRF)**: API framework for managing endpoints.
-   **PostgreSQL**: Database system for reliable data storage.
-   **Faker Library**: For generating fake book data.
-   **Bleach**: For input sanitization and security.
-   **Docker**: Containerization of the application.
-   **Docker Compose**: Orchestrates multiple containers.

----------

## Installation

Follow these steps to set up the project:

### Step 1: Clone the Repository

```bash
git clone git@github.com:ahmadsamir10/bookstore.git
cd bookstore

```

### Step 2: Build and Run Docker Containers

Ensure Docker and Docker Compose are installed on your system. Then, run:

```bash
docker-compose up --build

```

This command builds the Docker images and starts the services.

### Step 3: Superuser
***Username***: admin
***Email***: admin@gmail.com
***Password***: admin123

**Note**: You can change the Superuser details by editing the `./.envs/.django` Environmwnt Variables

----------

## Development Guide

### Adding Books

1.  **From Admin Panel**:  
    Log in to the admin panel at `http://localhost:8000/admin` and add books manually.
    
2.  **Using Management Command**:  
    Use the `add_book` command to add a book:
    
    ```bash
    docker-compose exec -it web python manage.py add_book --title "1984" --author "George Orwell" --description "A dystopian novel." --content "The full content of the book." --published_date 1949-06-08
    
    ```
    
3.  **Generating Fake Books**:  
    Use the `add_fake_books` command to generate multiple books:
    
    ```bash
    docker-compose exec -it web python manage.py add_fake_books 10
    
    ```
    

----------

## Project Structure

```
bookstore/
.
├── .envs
│	├── .django                  # Environment variables for Django settings
│	└── .postgres	             # Environment variables for PostgreSQL settings
		      
├── Dockerfile                   # Docker configuration for building the app container
├── docker-compose.yml           # Docker Compose configuration for multi-container setup
├── entrypoint.sh                # Entrypoint script for Docker
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies

├── bookstore/                   # Main Django project folder
│   ├── __init__.py
│   ├── asgi.py                  # ASGI configuration
│   ├── settings.py              # Django project settings
│   ├── urls.py                  # URL configuration for the project
│   └── wsgi.py                  # WSGI configuration

├── books/                       # Books app
│   ├── __init__.py
│   ├── admin.py                 # Admin configuration for books
│   ├── apps.py                  # App configuration for books
│   ├── models.py                # Models for books
│   ├── managers.py              # Custom model managers
│   ├── tests.py                 # Tests for books
│   ├── migrations/              # Database migrations for books
│   └── apis/                    # API-related files for books
│       ├── __init__.py
│       ├── serializers.py       # DRF serializers for books
│       ├── urls.py              # API routes for books
│       └── views.py             # API views for books

├── reviews/                     # Reviews app
│   ├── __init__.py
│   ├── admin.py                 # Admin configuration for reviews
│   ├── apps.py                  # App configuration for reviews
│   ├── models.py                # Models for reviews
│   ├── tests.py                 # Tests for reviews
│   ├── migrations/              # Database migrations for reviews
│   └── apis/                    # API-related files for reviews
│       ├── __init__.py
│       ├── serializers.py       # DRF serializers for reviews
│       ├── urls.py              # API routes for reviews
│       └── views.py             # API views for reviews

├── users/                       # Users app
│   ├── __init__.py
│   ├── admin.py                 # Admin configuration for users
│   ├── apps.py                  # App configuration for users
│   ├── models.py                # User model
│   ├── permissions.py           # Custom permissions
│   ├── validators.py            # Custom validators
│   ├── tests.py                 # Tests for users
│   ├── migrations/              # Database migrations for users
│   └── apis/                    # API-related files for users
│       ├── __init__.py
│       ├── serializers.py       # DRF serializers for users
│       ├── urls.py              # API routes for users
│       └── views.py             # API views for users
```

----------

## Entity-Relationship Diagram

![enter image description here](https://www.plantuml.com/plantuml/png/XP91IyD048Nl-HL3hzA3rvwAY222YBQd8c7QVRQZsTqwEx5AwtytqQJIa98zVjymlBVCD1chbRx844piY-O9ccYVKVKkI1nDw3OOrb1QFDmzD_n5D5aUs6D2JwOIreqek9-N2LfZQZajva7UIxGRuLcAitRBAUsYEkgiTMp8NwC4rEgQ3JFnoBwpjivLZ6_3TKoiG7StbxQ9sgKEQQMoDOcXKZDyMYDMCHY2dJ856rpErf_k4H-2tN2-PTKYFvKtHrb_xLcvYjvtKobRrUT_VYZitqaS3kDnt1yZJsXqIQbSUh54zwEi_kZ-eGt_3amHN7rdFm00)

----------

## API Documentation
Import Postman Collection From Here: [bookstore-Postman](https://documenter.getpostman.com/view/32404320/2sAYBUCXYD)

----------
