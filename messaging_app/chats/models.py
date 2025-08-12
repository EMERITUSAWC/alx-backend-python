# chats/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # ALX: Best practice to get the active user model

class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    Participants are linked via a ManyToMany relationship.
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at'] # Order by most recent activity

    def __str__(self):
        # ALX: A helpful string representation for admin and debugging
        participant_names = ", ".join([p.username for p in self.participants.all()])
        return f"Conversation {self.id} (Participants: {participant_names})"

class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE, # If conversation is deleted, messages are too
        related_name='messages' # Allows accessing messages from a conversation instance: conversation.messages.all()
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # If sender is deleted, their messages are also deleted (consider SET_NULL if you want to keep messages from deleted users)
        related_name='sent_messages' # Allows accessing sent messages from a user instance: user.sent_messages.all()
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp'] # Messages within a conversation should be ordered chronologically

    def __str__(self):
        return f"Msg {self.id} from {self.sender.username} in Conv {self.conversation.id}"