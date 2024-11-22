from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from books.apis.serializers import BookListSerializer, BookDetailSerializer
from users.permissions import IsClient


class BookListView(ListAPIView):
    """
    View to list all books.
    """
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated, IsClient]

    def get_queryset(self):
        return Book.objects.with_average_rating().order_by('-published_date')


class BookDetailView(RetrieveAPIView):
    """
    View to retrieve detailed information about a single book.
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsClient]

    def get_queryset(self):
        return Book.objects.with_average_rating().filter(pk=self.kwargs['pk'])
