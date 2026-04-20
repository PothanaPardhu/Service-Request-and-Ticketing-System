from django.test import TestCase
from django.contrib.auth import get_user_model
from core.constants import UserRole, TicketStatus, TicketPriority
from .models import Ticket, TicketActivity
from .services import TicketService

User = get_user_model()

class TicketLifecycleTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin@test.com', 'pass123')
        self.agent = User.objects.create_user('agent@test.com', 'pass123', role=UserRole.AGENT)
        self.customer = User.objects.create_user('user@test.com', 'pass123', role=UserRole.USER)

    def test_ticket_creation_and_sla(self):
        data = {
            'title': 'Test Ticket',
            'description': 'Description',
            'priority': TicketPriority.CRITICAL
        }
        ticket = TicketService.create_ticket(self.customer, data)
        self.assertEqual(ticket.status, TicketStatus.OPEN)
        self.assertEqual(ticket.created_by, self.customer)
        # Critical SLA is 4 hours
        expected_due = ticket.created_at + timedelta(hours=4)
        # Allow some buffer for execution time
        self.assertLess((ticket.due_date - expected_due).total_seconds(), 5)

    def test_invalid_status_transition(self):
        ticket = TicketService.create_ticket(self.customer, {'title': 'T1', 'description': 'D1'})
        # Cannot jump from OPEN to RESOLVED
        with self.assertRaises(ValueError):
            TicketService.update_status(self.admin, ticket, TicketStatus.RESOLVED)

    def test_valid_status_transition(self):
        ticket = TicketService.create_ticket(self.customer, {'title': 'T1', 'description': 'D1'})
        TicketService.assign_ticket(self.admin, ticket, self.agent)
        self.assertEqual(ticket.status, TicketStatus.ASSIGNED)
        
        TicketService.update_status(self.agent, ticket, TicketStatus.IN_PROGRESS)
        self.assertEqual(ticket.status, TicketStatus.IN_PROGRESS)

from datetime import timedelta
