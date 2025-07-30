
from datetime import date
from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for the Book model.
    Displays title, author, publication date, and days since publication.
    Allows filtering by date and searching by title/author.
    """
    list_display = ('title', 'author', 'published_date', 'days_since_published')
    list_filter = ('published_date',)
    search_fields = ('title', 'author')

    def days_since_published(self, obj):
        """
        Calculate and return the number of days since the book was published.
        Returns None if published_date is not set.
        """
        if obj.published_date:
            return (date.today() - obj.published_date).days
        return None

    days_since_published.short_description = 'Days Published'