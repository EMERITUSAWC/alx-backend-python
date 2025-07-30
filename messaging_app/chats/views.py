# chats/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers # Import serializers for ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination
from django.db.models import Q # Useful for more complex queries if needed

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    - Users can only see/interact with conversations they are a participant of.
    - The creator of a conversation is automatically added as a participant.
    """
    # ALX FIX: Add a default queryset for the router to infer basename
    queryset = Conversation.objects.all() # <--- ADD THIS LINE
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation] # Apply authentication and custom permission

    def get_queryset(self):
        """
        ALX: Override queryset to ensure users only see conversations they are part of.
        This is a critical security step for list views.
        """
        if self.request.user.is_authenticated:
            # Filter conversations where the current user is a participant
            return Conversation.objects.filter(participants=self.request.user).distinct()
        return Conversation.objects.none() # Return empty queryset for unauthenticated users

    def perform_create(self, serializer):
        """
        ALX: Custom creation logic to automatically add the current user as a participant.
        """
        conversation = serializer.save() # Save the conversation instance
        conversation.participants.add(self.request.user) # Add the requesting user as a participant
        conversation.save() # Save changes to the participants ManyToMany field


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    - Users can only interact with messages within conversations they are a participant of.
    - Sender is automatically set to the authenticated user.
    """
    # ALX FIX: Add a default queryset for the router to infer basename
    queryset = Message.objects.all() # <--- ADD THIS LINE
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation] # Apply authentication and custom permission
    filter_backends = [DjangoFilterBackend] # Enable filtering
    filterset_class = MessageFilter # Specify the filter class
    pagination_class = MessagePagination # Specify the pagination class

    def get_queryset(self):
        """
        ALX: Override queryset to ensure messages are only from conversations
        the current user is a part of. Messages are ordered chronologically.
        `select_related` is used for performance optimization.
        """
        if self.request.user.is_authenticated:
            # Filter messages where the associated conversation includes the current user
            return Message.objects.filter(
                conversation__participants=self.request.user
            ).select_related('sender', 'conversation').order_by('timestamp') # Optimize query and order
        return Message.objects.none() # Return empty queryset for unauthenticated users

    def perform_create(self, serializer):
        """
        ALX: Custom creation logic to automatically set the sender of the message
        to the current authenticated user and ensure the message is for a valid conversation
        that the user is a participant of.
        """
        # Get the conversation ID from the request data
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            raise serializers.ValidationError({"conversation": "Conversation ID is required."})

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError({"conversation": "Conversation not found."})

        # ALX: Crucial validation: User must be a participant of the target conversation
        if self.request.user not in conversation.participants.all():
            raise serializers.ValidationError({"conversation": "You are not a participant of this conversation."})

        # Save the message, linking the current user as sender and the validated conversation
        serializer.save(sender=self.request.user, conversation=conversation)