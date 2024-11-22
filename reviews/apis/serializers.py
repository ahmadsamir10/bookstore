from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from reviews.models import Review
from books.models import Book


class ReviewSerializer(serializers.ModelSerializer):
    # Assuming you want the user's string representation
    user = serializers.SerializerMethodField(method_name='get_user_fullname')

    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment', 'created_at']

    def get_user_fullname(self, obj):
        return obj.user.full_name


class CreateReviewSerializer(serializers.ModelSerializer):
    # Accept book_id in the request body
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['book_id', 'book', 'rating', 'comment']
        extra_kwargs = {'book': {'read_only': True}, 'rating': {
            'required': True}, 'comment': {'required': False}}

    def validate_book_id(self, value):
        """
        Validate if the book_id exists in the database.
        Raise a 404 error if not found.
        """
        book = Book.objects.filter(id=value).first()
        if not book:
            raise NotFound(detail=_("Book not found."))
        return value

    def create(self, validated_data):
        # Retrieve the book using the validated book_id
        book_id = validated_data.pop('book_id')
        # Get the book object using the book_id
        book = Book.objects.get(id=book_id)

        # Get context object
        context = self.context.get('request')

        # Add the user and the book to the validated data
        validated_data.update({
            'user': context.user,
            'book': book
        })

        return super().create(validated_data)
