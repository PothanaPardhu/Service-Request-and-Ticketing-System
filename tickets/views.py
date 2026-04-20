from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Ticket, TicketActivity
from .serializers import TicketSerializer, TicketCreateSerializer, CommentSerializer
from .services import TicketService
from core.permissions import IsAdmin, IsAgent, IsOwner, IsAssignedAgent, IsAdminOrAgent
from core.constants import UserRole, TicketStatus
from comments.models import Comment

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related('created_by', 'assigned_to').prefetch_related('activities', 'comments', 'comments__author')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority', 'due_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrAgent() | IsOwner()]
        if self.action == 'assign':
            return [IsAdmin()]
        if self.action in ['update_status', 'add_comment']:
            return [IsAdminOrAgent() | IsOwner()]
        if self.action == 'pick':
            return [IsAgent()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.ADMIN:
            return self.queryset
        if user.role == UserRole.AGENT:
            # Agents see tickets assigned to them or unassigned
            return self.queryset.filter(Q(assigned_to=user) | Q(assigned_to__isnull=True))
        # Customers see only their own tickets
        return self.queryset.filter(created_by=user)

    def perform_create(self, serializer):
        TicketService.create_ticket(self.request.user, serializer.validated_data)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        new_status = request.data.get('status')
        try:
            TicketService.update_status(request.user, ticket, new_status)
            return Response(TicketSerializer(ticket).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='assign')
    def assign(self, request, pk=None):
        ticket = self.get_object()
        agent_id = request.data.get('agent_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            agent = User.objects.get(id=agent_id, role=UserRole.AGENT)
            TicketService.assign_ticket(request.user, ticket, agent)
            return Response(TicketSerializer(ticket).data)
        except User.DoesNotExist:
            return Response({"error": "Valid Agent not found."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='comments')
    def add_comment(self, request, pk=None):
        ticket = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, ticket=ticket)
            # Log the comment activity
            TicketActivity.objects.create(
                ticket=ticket,
                performed_by=request.user,
                action_type='COMMENT',
                new_value="Comment added"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='unassigned')
    def unassigned(self, request):
        tickets = self.queryset.filter(assigned_to__isnull=True, status=TicketStatus.OPEN)
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='pick')
    def pick(self, request, pk=None):
        ticket = self.get_object()
        if ticket.assigned_to:
            return Response({"error": "Ticket already assigned."}, status=status.HTTP_400_BAD_REQUEST)
        TicketService.assign_ticket(request.user, ticket, request.user)
        return Response(TicketSerializer(ticket).data)
