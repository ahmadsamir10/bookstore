from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from books.managers import BookManager


class Book(models.Model):
    """
    Model to represent a book in the system.
    """
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    author = models.CharField(max_length=255, verbose_name=_("Author"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    content = models.TextField(verbose_name=_("Content"), blank=True)
    published_date = models.DateField(
        verbose_name=_("Published Date"), default=timezone.now)

    objects = BookManager()

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['-published_date', ]

    def __str__(self):
        return self.title

    @property
    def review_count(self):
        """
        Count all the reviews for a single book object
        """
        return self.reviews.count()
