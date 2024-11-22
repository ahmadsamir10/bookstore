from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from reviews.models import Review
from reviews.apis.serializers import ReviewSerializer, CreateReviewSerializer
from books.models import Book
from users.permissions import IsClient


class BookReviewsListView(ListAPIView):
    """
    View to list all reviews for a book.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsClient]

    def get_queryset(self):
        """
        This method filters the reviews based on the book's id passed in the URL.
        It raises a 404 error if the book does not exist.
        """
        # Get the book with the given book_id; raises 404 if not found
        book_id = self.kwargs['book_id']
        book = get_object_or_404(Book, id=book_id)

        # Return the reviews for the found book
        return Review.objects.filter(book_id=book.id).select_related('user').order_by('-created_at')


class CreateReviewView(CreateAPIView):
    """
    View to create a review for a book.
    """
    serializer_class = CreateReviewSerializer
    permission_classes = [IsAuthenticated, IsClient]
