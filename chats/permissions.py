from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to access messages.
    """
    def has_object_permission(self, request, view, obj):
        return obj.conversation.participants.filter(id=request.user.id).exists()