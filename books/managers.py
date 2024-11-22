from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from django.db import models


class BookManager(models.Manager):
    def with_average_rating(self):
        return self.prefetch_related('reviews').annotate(
            average_rating=Coalesce(
                Avg('reviews__rating'), Value(0, output_field=FloatField()))
        )
