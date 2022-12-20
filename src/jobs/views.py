from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, F
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from . import models


class JobListView(LoginRequiredMixin, ListView):
    context_object_name = "jobs"
    model = models.Job

    def get_queryset(self):
        return super(JobListView, self).get_queryset().filter(user=self.request.user).annotate(
            count=Count("periods"),
        )


class JobCreateView(LoginRequiredMixin, CreateView):
    model = models.Job
    fields = ["title", "currency", "hourly_rate"]
    success_url = reverse_lazy("job_table")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Job
    fields = ["title", "currency", "hourly_rate"]
    success_url = reverse_lazy("job_table")


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Job
    success_url = reverse_lazy("job_table")


class PeriodListView(LoginRequiredMixin, ListView):
    context_object_name = "periods"
    model = models.Period

    def get_queryset(self):
        return (
            super(PeriodListView, self)
            .get_queryset()
            .filter(job=self.kwargs.get("job_pk"))
            .annotate(
                count=Count("shifts"),
                hours=Sum("shifts__length"),
                income=Sum("shifts__length") * F("job__hourly_rate"),
            )
            .order_by("-cutoff")
        )


class PeriodCreateView(LoginRequiredMixin, CreateView):
    model = models.Period
    fields = ["cutoff", "payday"]

    def form_valid(self, form):
        form.instance.job = models.Job.objects.get(
            pk=self.kwargs.get("job_pk"))
        return super(PeriodCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("period_list", kwargs=self.kwargs)


class PeriodUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Period
    fields = "__all__"

    def get_success_url(self):
        return reverse(
            "period_list",
            kwargs={
                "job_pk": self.object.job.id,
            }
        )


class PeriodDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Period

    def get_success_url(self):
        return reverse(
            "period_list",
            kwargs={
                "job_pk": self.object.job.id,
            }
        )


class ShiftListView(LoginRequiredMixin, ListView):
    model = models.Shift
    context_object_name = "shifts"

    def get_queryset(self):
        return super(ShiftListView, self).get_queryset().filter(period=self.kwargs.get("period_pk")).annotate(
            income=F("length") * F("period__job__hourly_rate")
        )


class ShiftCreateView(LoginRequiredMixin, CreateView):
    model = models.Shift
    fields = ["start", "finish"]

    def form_valid(self, form):
        form.instance.period = models.Period.objects.get(
            pk=self.kwargs.get("period_pk"))
        delta = form.instance.finish - form.instance.start
        form.instance.length = delta.total_seconds() / (60 * 60)
        return super(ShiftCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("shift_list", kwargs=self.kwargs)


class ShiftCreateViewAlt(ShiftCreateView):
    fields = ["start", "length"]

    def form_valid(self, form):
        form.instance.finish = form.instance.start + \
            timedelta(hours=form.instance.length)
        return super(ShiftCreateViewAlt, self).form_valid(form)


class ShiftUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Shift
    fields = ["period", "start", "finish"]

    def form_valid(self, form):
        delta = form.instance.finish - form.instance.start
        form.instance.length = delta.total_seconds() / (60 * 60)
        return super(ShiftUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "shift_list",
            kwargs={
                "job_pk": self.object.period.job.id,
                "period_pk": self.object.period.id
            }
        )


class ShiftUpdateViewAlt(ShiftUpdateView):
    fields = ["period", "start", "length"]

    def form_valid(self, form):
        form.instance.finish = form.instance.start + \
            timedelta(hours=form.instance.length)
        return super(ShiftUpdateViewAlt, self).form_valid(form)


class ShiftDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Shift
    success_url = reverse_lazy("job_table")

    def get_success_url(self):
        return reverse(
            "shift_list",
            kwargs={
                "job_pk": self.object.period.job.id,
                "period_pk": self.object.period.id
            }
        )
