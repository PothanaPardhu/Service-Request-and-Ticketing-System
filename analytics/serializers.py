from rest_framework import serializers

class AnalyticsSerializer(serializers.Serializer):
    total_tickets = serializers.IntegerField()
    status_distribution = serializers.DictField(child=serializers.IntegerField())
    priority_distribution = serializers.DictField(child=serializers.IntegerField())
    overdue_count = serializers.IntegerField()
    avg_resolution_hours = serializers.FloatField()
    agent_performance = serializers.ListField(child=serializers.DictField())
