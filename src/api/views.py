from jobs import models
from rest_framework import viewsets, permissions
from . import serializers


class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = [permissions.IsAuthenticated]


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = models.Period.objects.all()
    serializer_class = serializers.PeriodSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = models.Shift.objects.all()
    serializer_class = serializers.ShiftSerializer
    permission_classes = [permissions.IsAuthenticated]
