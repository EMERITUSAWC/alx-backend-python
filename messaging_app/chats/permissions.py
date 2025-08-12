# chats/permissions.py
from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to
    view, update, or delete messages and the conversation itself.
    """
    message = 'You are not a participant of this conversation.' # ALX: Custom error message for better API feedback

    def has_permission(self, request, view):
        """
        Global permission check: Ensure the user is authenticated for any operation
        on conversation/message related endpoints.
        """
        # ALX: This check ensures that if the user isn't authenticated,
        # they won't even proceed to object-level permission checks.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check:
        - For Conversation instances: Check if the requesting user is a participant.
        - For Message instances: Check if the requesting user is a participant of the
          conversation associated with the message.
        """
        # Ensure the user is authenticated before checking object permissions
        if not (request.user and request.user.is_authenticated):
            return False

        # Check if the object is a Conversation or a Message
        if isinstance(obj, Conversation):
            # For a Conversation object, check if the user is in its participants
            return request.user in obj.participants.all()
        elif isinstance(obj, Message):
            # For a Message object, check if the user is a participant of its related Conversation
            return request.user in obj.conversation.participants.all()

        # If it's neither a Conversation nor a Message, deny access by default
        return False