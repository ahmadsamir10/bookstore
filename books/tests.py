from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book
from users.models import User
from rest_framework.authtoken.models import Token
from datetime import date
from books.apis.serializers import BookListSerializer, BookDetailSerializer


class BookListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/books/"
        # Create a user and authenticate
        self.user = User.objects.create_user(first_name="Ahmad", last_name="Samir", email="testuser@example.com",
                                             username="testuser", user_type="client", password="Password123!")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create books
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            description="Description of Book One",
            published_date=date(2023, 1, 1),
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            description="Description of Book Two",
            published_date=date(2022, 1, 1),
        )

    def test_book_list_valid(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results')
        self.assertEqual(len(result), 2)
        # Check if the 'average_rating' field is in the response
        self.assertIn('average_rating', result[0])

    def test_book_list_not_authenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a book
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            description="Description of Book One",
            content="Content of Book One",
            published_date=date(2023, 1, 1),
        )
        # Create a user and authenticate
        self.user = User.objects.create_user(first_name="Ahmad", last_name="Samir", email="testuser@example.com",
                                             username="testuser", user_type="client", password="Password123!")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.url = "/api/v1/books/{}/".format(self.book1.pk)

    def test_book_detail_valid(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.book1.id)
        self.assertIn('average_rating', response.data)
        self.assertIn('review_count', response.data)

    def test_book_detail_not_authenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookSerializerTests(TestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'content': 'Test Content',
            'published_date': date(2023, 1, 1),
        }
        book_created = Book.objects.create(**self.book_data)
        self.book = Book.objects.with_average_rating().filter(pk=book_created.pk).first()

    def test_book_list_serializer(self):
        serializer = BookListSerializer(self.book)
        self.assertEqual(serializer.data['title'], self.book.title)
        self.assertEqual(serializer.data['author'], self.book.author)
        self.assertEqual(serializer.data['description'], self.book.description)
        # Check if the 'average_rating' field is present
        self.assertIn('average_rating', serializer.data)

    def test_book_detail_serializer(self):
        serializer = BookDetailSerializer(self.book)
        self.assertEqual(serializer.data['title'], self.book.title)
        self.assertEqual(serializer.data['author'], self.book.author)
        self.assertEqual(serializer.data['description'], self.book.description)
        self.assertEqual(serializer.data['content'], self.book.content)
        self.assertEqual(serializer.data['published_date'], str(
            self.book.published_date))
        # Check if the 'average_rating' and 'review_count' fields are present
        self.assertIn('average_rating', serializer.data)
        self.assertIn('review_count', serializer.data)


class BookModelTests(TestCase):
    def setUp(self):
        # Create a book with no reviews
        book_created = Book.objects.create(
            title="Book Without Reviews",
            author="No Reviews Author",
            description="This book has no reviews.",
            content="Some content here.",
            published_date=date(2023, 1, 1),
        )
        self.book = Book.objects.with_average_rating().filter(pk=book_created.pk).first()

    def test_review_count(self):
        # Ensure the review count is 0 when no reviews are present
        self.assertEqual(self.book.review_count, 0)

    def test_average_rating(self):
        # Ensure the average rating is 0 when no reviews are present
        self.assertEqual(self.book.average_rating, 0.00)


class BookManagerTests(TestCase):
    def setUp(self):
        # Create a user to add review with
        self.user = User.objects.create_user(first_name="Ahmad", last_name="Samir", email="testuser@example.com",
                                             username="testuser", user_type="client", password="Password123!")
        # Create books and their respective reviews
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            description="Description of Book One",
            published_date=date(2023, 1, 1),
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            description="Description of Book Two",
            published_date=date(2022, 1, 1),
        )

        # Adding some reviews to book1
        self.book1.reviews.create(user=self.user, rating=4)
        self.book1.reviews.create(user=self.user, rating=5)

    def test_with_average_rating(self):
        books = Book.objects.with_average_rating()
        self.assertEqual(books.count(), 2)
        # Average of book1's ratings
        self.assertEqual(books.first().average_rating, 4.5)
        self.assertEqual(books.last().average_rating,
                         0.00)  # No reviews for book2
