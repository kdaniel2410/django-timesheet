from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    currency = models.CharField(max_length=1, default="£")
    hourly_rate = models.FloatField(default=9.18)

    def __str__(self):
        return f"{self.company} {self.title}"

    class Meta:
        ordering = ["company", "title"]


class Period(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cutoff = models.DateField()
    payday = models.DateField()

    def __str__(self):
        return f"{self.job} {self.cutoff}"

    class Meta:
        ordering = ["-cutoff"]


class Shift(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    start = models.DateTimeField(default=datetime.now)
    length = models.FloatField(default=7)

    @property
    def income(self):
        return self.period.job.hourly_rate * self.length

    def __str__(self):
        return f"{self.length} hours on {self.start}"

    class Meta:
        ordering = ["-start"]
