from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatRoom(models.Model):
    ROOM_TYPES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
    ]
    
    name = models.CharField(max_length=255, blank=True, null=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='direct')
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    
    def __str__(self):
        if self.name:
            return self.name
        # For direct messages, show participant names
        participants = list(self.participants.all())
        if len(participants) == 2:
            return f"{participants[0].username} & {participants[1].username}"
        return f"Chat {self.id}"
    
    def save(self, *args, **kwargs):
        # Auto-generate name for direct messages
        if self.room_type == 'direct' and not self.name:
            participants = list(self.participants.all())
            if len(participants) == 2:
                self.name = f"{participants[0].username} & {participants[1].username}"
        super().save(*args, **kwargs)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f'{self.sender.username}: {self.content[:50]}'