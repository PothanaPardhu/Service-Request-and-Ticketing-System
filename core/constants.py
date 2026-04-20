from django.db import models

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    AGENT = 'AGENT', 'Agent'
    USER = 'USER', 'User'

class TicketStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'

class TicketPriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'

class ActionType(models.TextChoices):
    STATUS_CHANGE = 'STATUS_CHANGE', 'Status Change'
    ASSIGNMENT = 'ASSIGNMENT', 'Assignment'
    COMMENT = 'COMMENT', 'Comment'
    PRIORITY_CHANGE = 'PRIORITY_CHANGE', 'Priority Change'
    SLA_BREACH = 'SLA_BREACH', 'SLA Breach'
