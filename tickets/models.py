from django.db import models
from django.conf import settings
from core.constants import TicketStatus, TicketPriority, ActionType

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=TicketStatus.choices, 
        default=TicketStatus.OPEN
    )
    priority = models.CharField(
        max_length=20, 
        choices=TicketPriority.choices, 
        default=TicketPriority.MEDIUM
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_tickets'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets'
    )
    due_date = models.DateTimeField()
    resolved_at = models.DateTimeField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.title} ({self.status})"

    class Meta:
        ordering = ['-created_at']

class TicketActivity(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='activities'
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    action_type = models.CharField(
        max_length=20, 
        choices=ActionType.choices
    )
    old_value = models.CharField(max_length=255, null=True, blank=True)
    new_value = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} on #{self.ticket.id} by {self.performed_by.email}"

    class Meta:
        verbose_name_plural = "Ticket Activities"
        ordering = ['-timestamp']
