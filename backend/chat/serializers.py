from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatRoom, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source='participants'
    )
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'created_at', 'participants', 'participant_ids']
        read_only_fields = ['created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='sender'
    )
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_id', 'content', 'timestamp', 'is_read']
        read_only_fields = ['timestamp', 'is_read']

class CreateDirectChatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return value