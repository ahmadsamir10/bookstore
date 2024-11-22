import bleach
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Review(models.Model):
    """
    Model to represent a user's review for a book.
    """
    book = models.ForeignKey(
        'books.Book', on_delete=models.CASCADE, related_name='reviews', db_index=True, verbose_name=_("Book"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', db_index=True, verbose_name=_("User"))
    rating = models.PositiveIntegerField(
        verbose_name=_("Rating"), choices=[(i, i) for i in range(1, 6)], default=1)
    comment = models.TextField(verbose_name=_("Comment"), blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user} for {self.book.title}"

    def save(self, *args, **kwargs):
        # Sanitize the comment field using bleach before saving
        if self.comment:
            self.comment = bleach.clean(
                self.comment, tags=['b', 'i', 'u', 'em', 'strong'], attributes={}, strip=True)
        super().save(*args, **kwargs)
