from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from .models import ChatRoom, Message
from .serializers import (
    ChatRoomSerializer, 
    MessageSerializer, 
    UserSerializer,
    CreateDirectChatSerializer
)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Exclude current user from list
        return User.objects.exclude(id=self.request.user.id)

class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return only rooms where user is a participant
        user = self.request.user
        return ChatRoom.objects.filter(participants=user)
    
    def perform_create(self, serializer):
        # Automatically add current user to participants
        chat_room = serializer.save()
        if self.request.user not in chat_room.participants.all():
            chat_room.participants.add(self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_direct_chat(self, request):
        """
        Create or get existing direct chat with another user
        """
        serializer = CreateDirectChatSerializer(data=request.data)
        if serializer.is_valid():
            other_user_id = serializer.validated_data['user_id']
            
            # Check if direct chat already exists
            existing_chat = ChatRoom.objects.filter(
                room_type='direct',
                participants=request.user
            ).filter(
                participants__id=other_user_id
            ).distinct()
            
            if existing_chat.exists():
                chat_room = existing_chat.first()
            else:
                # Create new direct chat
                other_user = User.objects.get(id=other_user_id)
                chat_room = ChatRoom.objects.create(room_type='direct')
                chat_room.participants.add(request.user, other_user)
                chat_room.save()
            
            return Response(
                ChatRoomSerializer(chat_room, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages for a specific chat room
        """
        chat_room = self.get_object()
        messages = chat_room.messages.all()
        
        # Mark messages from others as read
        unread_messages = messages.filter(
            sender__id__ne=request.user.id,
            is_read=False
        )
        unread_messages.update(is_read=True)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # User can only see messages from rooms they're in
        user_rooms = ChatRoom.objects.filter(participants=self.request.user)
        return Message.objects.filter(room__in=user_rooms)
    
    def perform_create(self, serializer):
        # Automatically set sender to current user
        serializer.save(sender=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_message_count(request):
    """
    Get count of unread messages for the current user
    """
    user_rooms = ChatRoom.objects.filter(participants=request.user)
    unread_count = Message.objects.filter(
        room__in=user_rooms,
        sender__id__ne=request.user.id,
        is_read=False
    ).count()
    
    return Response({'unread_count': unread_count})