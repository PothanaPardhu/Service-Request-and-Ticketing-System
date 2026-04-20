from rest_framework import serializers
from .models import Ticket, TicketActivity
from users.serializers import UserSerializer
from comments.models import Comment

class TicketActivitySerializer(serializers.ModelSerializer):
    performed_by = UserSerializer(read_only=True)

    class Meta:
        model = TicketActivity
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'ticket', 'author', 'message', 'created_at')
        read_only_fields = ('author', 'created_at')

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    activities = TicketActivitySerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id', 'title', 'description', 'status', 'priority', 
            'created_by', 'assigned_to', 'due_date', 'resolved_at', 
            'is_overdue', 'created_at', 'updated_at', 'activities', 'comments'
        )
        read_only_fields = (
            'created_by', 'due_date', 'resolved_at', 
            'is_overdue', 'created_at', 'updated_at'
        )

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority')
