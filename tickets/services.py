from datetime import timedelta
from django.utils import timezone
from core.constants import TicketStatus, TicketPriority, ActionType
from .models import Ticket, TicketActivity

class TicketService:
    ALLOWED_TRANSITIONS = {
        TicketStatus.OPEN: [TicketStatus.ASSIGNED, TicketStatus.CLOSED],
        TicketStatus.ASSIGNED: [TicketStatus.IN_PROGRESS, TicketStatus.OPEN],
        TicketStatus.IN_PROGRESS: [TicketStatus.RESOLVED],
        TicketStatus.RESOLVED: [TicketStatus.CLOSED, TicketStatus.IN_PROGRESS],
        TicketStatus.CLOSED: [TicketStatus.OPEN], # Allowing reopening
    }

    SLA_HOURS = {
        TicketPriority.CRITICAL: 4,
        TicketPriority.HIGH: 24,
        TicketPriority.MEDIUM: 48,
        TicketPriority.LOW: 72,
    }

    @staticmethod
    def calculate_due_date(priority):
        hours = TicketService.SLA_HOURS.get(priority, 48)
        return timezone.now() + timedelta(hours=hours)

    @staticmethod
    def create_ticket(user, data):
        priority = data.get('priority', TicketPriority.MEDIUM)
        due_date = TicketService.calculate_due_date(priority)
        
        ticket = Ticket.objects.create(
            created_by=user,
            due_date=due_date,
            **data
        )
        
        TicketActivity.objects.create(
            ticket=ticket,
            performed_by=user,
            action_type=ActionType.STATUS_CHANGE,
            new_value=TicketStatus.OPEN
        )
        return ticket

    @staticmethod
    def update_status(user, ticket, new_status):
        if new_status not in TicketService.ALLOWED_TRANSITIONS.get(ticket.status, []):
            raise ValueError(f"Transition from {ticket.status} to {new_status} is not allowed.")

        old_status = ticket.status
        ticket.status = new_status
        
        if new_status == TicketStatus.RESOLVED:
            ticket.resolved_at = timezone.now()
            # Check if resolved before due_date
            if ticket.resolved_at > ticket.due_date:
                ticket.is_overdue = True
        
        ticket.save()

        TicketActivity.objects.create(
            ticket=ticket,
            performed_by=user,
            action_type=ActionType.STATUS_CHANGE,
            old_value=old_status,
            new_value=new_status
        )
        return ticket

    @staticmethod
    def assign_ticket(user, ticket, agent):
        old_agent = ticket.assigned_to.email if ticket.assigned_to else "None"
        ticket.assigned_to = agent
        
        # If manually assigned, automatically move to ASSIGNED status if it was OPEN
        if ticket.status == TicketStatus.OPEN:
            ticket.status = TicketStatus.ASSIGNED
            
        ticket.save()

        TicketActivity.objects.create(
            ticket=ticket,
            performed_by=user,
            action_type=ActionType.ASSIGNMENT,
            old_value=old_agent,
            new_value=agent.email
        )
        return ticket
