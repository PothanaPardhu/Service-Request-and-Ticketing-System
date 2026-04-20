from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Avg, F, Q
from tickets.models import Ticket
from core.constants import TicketStatus, UserRole
from core.permissions import IsAdmin

from .serializers import AnalyticsSerializer

class DashboardAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = AnalyticsSerializer

    def get(self, request):
        total_tickets = Ticket.objects.count()
        status_counts = Ticket.objects.values('status').annotate(count=Count('status'))
        priority_counts = Ticket.objects.values('priority').annotate(count=Count('priority'))
        
        overdue_tickets = Ticket.objects.filter(is_overdue=True).count()
        
        # Average resolution time in hours
        avg_resolution_time = Ticket.objects.filter(
            status=TicketStatus.RESOLVED,
            resolved_at__isnull=False
        ).annotate(
            duration=F('resolved_at') - F('created_at')
        ).aggregate(avg_time=Avg('duration'))['avg_time']

        if avg_resolution_time:
            avg_resolution_hours = avg_resolution_time.total_seconds() / 3600
        else:
            avg_resolution_hours = 0

        agent_performance = Ticket.objects.filter(
            assigned_to__isnull=False
        ).values(
            'assigned_to__email'
        ).annotate(
            tickets_handled=Count('id'),
            resolved=Count('id', filter=Q(status=TicketStatus.RESOLVED))
        )

        return Response({
            "total_tickets": total_tickets,
            "status_distribution": {item['status']: item['count'] for item in status_counts},
            "priority_distribution": {item['priority']: item['count'] for item in priority_counts},
            "overdue_count": overdue_tickets,
            "avg_resolution_hours": round(avg_resolution_hours, 2),
            "agent_performance": agent_performance
        })
