from rest_framework import serializers
from jobs import models


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = ["title", "currency", "hourly_rate"]


class PeriodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Period
        fields = '__all__'


class ShiftSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Shift
        fields = '__all__'
