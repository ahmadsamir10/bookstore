from faker import Faker
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from books.models import Book


class Command(BaseCommand):
    """
    Generates a specified number of books with fake data using the Faker library.

    Populates the following fields for each book:
    - title: Random sentence (5 words).
    - author: Random full name.
    - description: Random text (up to 500 characters).
    - content: Random text (up to 2000 characters).
    - published_date: Random date within the last 10 years.

    Usage:
        python manage.py add_fake_books <count>

    Example:
        python manage.py add_fake_books 10  # Generates 10 books.

    Dependencies:
    - Faker library.
    """
    help = "Generate N books with fake data"

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help="Number of books to generate"
        )

    def handle(self, *args, **options):
        count = options['count']
        faker = Faker()

        for _ in range(count):
            title = faker.sentence(nb_words=5)
            author = faker.name()
            description = faker.text(max_nb_chars=500)
            content = faker.text(max_nb_chars=2000)
            published_date = faker.date_between(
                start_date="-10y",
                end_date=now().date()
            )

            # Create the book
            Book.objects.create(
                title=title,
                author=author,
                description=description,
                content=content,
                published_date=published_date,
            )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {count} fake books."))
