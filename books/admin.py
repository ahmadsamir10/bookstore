from django.contrib import admin
from books.models import Book
from django.utils.translation import gettext_lazy as _


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'description_excerpt')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'author')
    ordering = ('-published_date',)
    readonly_fields = ('description_excerpt',)

    # Custom method to show a short excerpt of the description
    def description_excerpt(self, obj):
        return obj.description[:100] + '...' if obj.description else ''
    description_excerpt.short_description = _('Description Excerpt')


admin.site.register(Book, BookAdmin)
