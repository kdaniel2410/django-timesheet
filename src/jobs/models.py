from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    currency = models.CharField(max_length=1, default="£")
    hourly_rate = models.FloatField(default=9.18)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Period(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cutoff = models.DateField()
    payday = models.DateField()

    def __str__(self):
        return self.cutoff.strftime(f"%B")


class Shift(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    length = models.FloatField(default=0)
    income = models.FloatField()

    def save(self, *args, **kwargs):
        self.income = self.length * self.period.job.hourly_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.start.strftime("%a %d/%m/%y")

    class Meta:
        ordering = ["-start"]
