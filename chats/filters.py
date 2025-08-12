import django_filters
from .models import Message
from django_filters import rest_framework as filters

class MessageFilter(filters.FilterSet):
    conversation = filters.NumberFilter(field_name='conversation')
    sender = filters.NumberFilter(field_name='sender')
    created_at__gte = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'created_at__gte', 'created_at__lte']