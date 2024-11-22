from django.urls import path
from reviews.apis import views

api_v1_prefix = "api/v1"

urlpatterns = [
    path(f'{api_v1_prefix}/books/<int:book_id>/reviews/',
         views.BookReviewsListView.as_view(), name='book-reviews-list'),
    path(f'{api_v1_prefix}/books/reviews/create/',
         views.CreateReviewView.as_view(), name='create-review'),
]
