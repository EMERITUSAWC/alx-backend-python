# chats/filters.py
import django_filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for the Message model, allowing filtering by:
    - `sender_username`: Case-insensitive partial match on sender's username.
    - `content_contains`: Case-insensitive partial match on message content.
    - `timestamp_after`/`timestamp_before`: Date/time range filtering for messages.
    - `conversation`: Filter by specific conversation ID.
    """
    sender_username = django_filters.CharFilter(
        field_name='sender__username', lookup_expr='icontains',
        help_text="Filter messages by sender's username (case-insensitive contains)."
    )
    content_contains = django_filters.CharFilter(
        field_name='content', lookup_expr='icontains',
        help_text="Filter messages by content (case-insensitive contains)."
    )
    # ALX: Using DateTimeFromToRangeFilter for flexible date range queries
    timestamp = django_filters.DateTimeFromToRangeFilter(
        field_name='timestamp',
        help_text="Filter messages within a date/time range. Use timestamp_after=YYYY-MM-DDTHH:MM:SS and/or timestamp_before=YYYY-MM-DDTHH:MM:SS."
    )
    conversation = django_filters.ModelChoiceFilter(
        queryset=Conversation.objects.all(),
        help_text="Filter messages by specific conversation ID."
    )

    class Meta:
        model = Message
        # ALX: Explicitly list fields available for filtering for clarity and security
        fields = [
            'sender_username',
            'content_contains',
            'timestamp',
            'conversation'
        ]