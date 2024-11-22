from django.contrib import admin
from reviews.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at', 'comment')
    list_filter = ('rating', 'created_at', 'book', 'user')
    search_fields = ('user__email', 'book__title', 'comment')
    fieldsets = (
        (None, {'fields': ('book', 'user', 'rating', 'comment')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at', )
    ordering = ('-created_at',)


admin.site.register(Review, ReviewAdmin)
