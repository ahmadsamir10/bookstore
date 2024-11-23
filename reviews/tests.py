from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework import status
from reviews.models import Review
from books.models import Book
from users.models import User
from rest_framework.authtoken.models import Token
from reviews.apis.serializers import CreateReviewSerializer


class BookReviewsListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01"
        )
        self.user = User.objects.create_user(first_name="Ahmad", last_name="Samir", email="testuser@example.com",
                                             username="testuser", user_type="client", password="Password123!")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create some reviews for the book
        self.review1 = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=4,
            comment="Great book!"
        )
        self.review2 = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            comment="Excellent read!"
        )

        self.url = f"/api/v1/books/{self.book.id}/reviews/"

    def test_book_reviews_list_valid(self):
        response = self.client.get(self.url)
        result = response.data.get("results")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 2)
        self.assertIn('user', result[0])
        self.assertIn('rating', result[0])
        self.assertIn('comment', result[0])

    def test_book_reviews_list_empty(self):
        # Create a book with no reviews
        book_no_reviews = Book.objects.create(
            title="Another Test Book",
            author="Another Author",
            description="Another Test Description",
            published_date="2023-02-01"
        )
        response = self.client.get(
            f"/api/v1/books/{book_no_reviews.id}/reviews/")
        result = response.data.get("results")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 0)

    def test_book_reviews_list_not_authenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateReviewViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book for Review",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01"
        )
        self.user = User.objects.create_user(first_name="Ahmad", last_name="Samir", email="testuser@example.com",
                                             username="testuser", user_type="client", password="Password123!")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.url = "/api/v1/books/reviews/create/"

    def test_create_review_valid(self):
        data = {
            "book_id": self.book.id,
            "rating": 5,
            "comment": "Amazing book, highly recommended!"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['book'], self.book.id)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['comment'],
                         "Amazing book, highly recommended!")

    def test_create_review_book_not_found(self):
        data = {
            "book_id": 99999,  # Non-existent book ID
            "rating": 4,
            "comment": "This book doesn't exist."
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)

    def test_create_review_not_authenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "book_id": self.book.id,
            "rating": 5,
            "comment": "Amazing book!"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewSerializerTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01"
        )
        self.user = User.objects.create_user(first_name="Ahmad", last_name="Samir", email="testuser@example.com",
                                             username="testuser", user_type="client", password="Password123!")

        # Create a request and add the user to the context manually
        factory = APIRequestFactory()
        request = factory.post(
            '/fake-url/', {'book_id': self.book.id, 'rating': 5, 'comment': 'Fantastic book!'})
        request.user = self.user  # Add the user to the request context
        self.context = {'request': request}  # Pass the request to the context

    def test_create_review_serializer(self):
        data = {
            "book_id": self.book.id,
            "rating": 5,
            "comment": "Fantastic book!"
        }
        serializer = CreateReviewSerializer(
            data=data, context=self.context)  # Pass the context here
        self.assertTrue(serializer.is_valid())
        review = serializer.save()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Fantastic book!")
        self.assertEqual(review.book, self.book)


class ReviewModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book for Review",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01"
        )
        self.user = User.objects.create_user(first_name="Ahmad", last_name="Samir", email="testuser@example.com",
                                             username="testuser", user_type="client", password="Password123!")

    def test_review_creation(self):
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            comment="Wonderful book!"
        )
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Wonderful book!")

    def test_review_sanitization(self):
        # Create review with HTML tags in comment
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            comment="<script>alert('xss')</script><b>Great Book</b>"
        )
        # Check that the comment is sanitized
        self.assertNotIn("<script>", review.comment)
        # Allow some tags like <b>
        self.assertIn("<b>Great Book</b>", review.comment)
