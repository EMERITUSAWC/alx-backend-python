# chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    - `page_size`: The default number of messages per page.
    - `page_size_query_param`: Allows clients to specify page size (e.g., ?page_size=10).
    - `max_page_size`: Limits the maximum page size to prevent abuse.
    """
    page_size = 20 # Default number of messages per page
    page_size_query_param = 'page_size' # Query parameter name for page size
    max_page_size = 100 # Maximum allowed page size to prevent large requests