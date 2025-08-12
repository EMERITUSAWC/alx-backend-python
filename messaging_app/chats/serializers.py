# chats/serializers.py
from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Django User model.
    Used for displaying sender/participant details in a read-only manner.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['username', 'email', 'first_name', 'last_name'] # Ensure these cannot be set via this serializer

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Handles serialization/deserialization of message content.
    """
    sender = UserSerializer(read_only=True) # Display full sender object, but don't allow setting via input

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp'] # Sender and timestamp are set automatically by the server

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes nested messages and participants for read operations.
    """
    participants = UserSerializer(many=True, read_only=True) # Display participants as nested user objects
    messages = MessageSerializer(many=True, read_only=True) # Display messages as nested message objects (ordered by timestamp implicitly from model Meta)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] # Auto-managed fields