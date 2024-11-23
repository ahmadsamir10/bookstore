import sys
from django.core.management.base import BaseCommand
from books.models import Book
from django.utils.timezone import now


class Command(BaseCommand):
    """
    Command to add a new book to the system.

    Usage:
        python manage.py add_book --title "Book Title" --author "Author Name" 
                                [--description "Description"] [--content "Content"] 
                                [--published_date "YYYY-MM-DD"]

    Arguments:
        --title (str):          Title of the book (required).
        --author (str):         Author of the book (required).
        --description (str):    Book description (optional, defaults to empty).
        --content (str):        Book content (optional, defaults to empty).
        --published_date (str): Published date in "YYYY-MM-DD" format (optional, defaults to today).

    Example:
        python manage.py add_book --title "Sample Book" --author "John Doe" --description "A sample description."

    Outputs success or error messages based on input validation.
    """

    help = "Add a new book to the system"

    def add_arguments(self, parser):
        parser.add_argument('--title', type=str,
                            required=True, help="Title of the book")
        parser.add_argument('--author', type=str,
                            required=True, help="Author of the book")
        parser.add_argument('--description', type=str,
                            required=True, help="Description of the book")
        parser.add_argument('--content', type=str,
                            required=True, help="Content of the book")
        parser.add_argument('--published_date', type=str,
                            help="Published date (YYYY-MM-DD), optional", default=None)

    def handle(self, *args, **options):
        title = options['title']
        author = options['author']
        description = options['description']
        content = options['content']
        published_date = options['published_date']

        # Validate required fields
        if not title:
            self.stdout.write(self.style.ERROR(
                "The 'title' field is required."))
            sys.exit(1)

        if not author:
            self.stdout.write(self.style.ERROR(
                "The 'author' field is required."))
            sys.exit(1)

        if not description:
            self.stdout.write(self.style.ERROR(
                "The 'description' field is required."))
            sys.exit(1)

        if not content:
            self.stdout.write(self.style.ERROR(
                "The 'content' field is required."))
            sys.exit(1)

        # Handle published_date
        if not published_date:
            published_date = now().date()
        else:
            try:
                from datetime import datetime
                published_date = datetime.strptime(
                    published_date, "%Y-%m-%d").date()
            except ValueError:
                self.stdout.write(self.style.ERROR(
                    "Invalid date format. Use YYYY-MM-DD."))
                sys.exit(1)

        # Create the book
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            content=content,
            published_date=published_date,
        )

        self.stdout.write(self.style.SUCCESS(
            f"Book '{book.title}' by {book.author} added successfully."))
