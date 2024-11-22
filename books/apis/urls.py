from django.urls import path
from books.apis import views

api_v1_prefix = "api/v1"

urlpatterns = [
    path(f'{api_v1_prefix}/books/',
         views.BookListView.as_view(), name='book-list'),
    path(f'{api_v1_prefix}/books/<int:pk>/',
         views.BookDetailView.as_view(), name='book-detail'),
]
