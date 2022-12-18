from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from . import models


class JobTableView(LoginRequiredMixin, ListView):
    context_object_name = "jobs"
    model = models.Job
    template_name = 'jobs/job_table.html'

    def get_queryset(self):
        return super(JobTableView, self).get_queryset().filter(user=self.request.user)


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
                shifts=Count("shift"),
                hours=Sum("shift__length"),
                income=Sum("shift__income"),
            )
            .order_by("-cutoff")
        )


class PeriodTableView(PeriodListView):
    template_name = 'jobs/period_table.html'


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
        return super(ShiftListView, self).get_queryset().filter(period=self.kwargs.get("period_pk"))


class ShiftTableView(ShiftListView):
    template_name = 'jobs/shift_table.html'


class ShiftCreateView(LoginRequiredMixin, CreateView):
    model = models.Shift
    fields = ["start", "finish"]

    def form_valid(self, form):
        form.instance.period = models.Period.objects.get(
            pk=self.kwargs.get("period_pk"))
        return super(ShiftCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("shift_list", kwargs=self.kwargs)


class ShiftCreateViewAlt(ShiftCreateView):
    fields = ["start", "length"]


class ShiftUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Shift
    fields = ["period", "start", "finish"]

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
