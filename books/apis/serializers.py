from rest_framework import serializers
from books.models import Book


# Book List Serializer
class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing books (limited fields).
    """
    average_rating = serializers.SerializerMethodField(
        method_name='calculate_average_rating')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'average_rating']

    def calculate_average_rating(self, obj):
        # Round the average_rating to the nearest 0.5
        return round(obj.average_rating * 2) / 2 if obj.average_rating is not None else 0.00


# Book Details Serializer
class BookDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a book's details (all fields).
    """
    average_rating = serializers.SerializerMethodField(
        method_name='calculate_average_rating')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author',
                  'description', 'content', 'average_rating', 'review_count', 'published_date']

    def calculate_average_rating(self, obj):
        # Round the average_rating to the nearest 0.5
        return round(obj.average_rating * 2) / 2 if obj.average_rating is not None else 0.00
