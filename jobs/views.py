from . import models
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F, Sum


class JobListView(LoginRequiredMixin, ListView):
    context_object_name = "jobs"
    model = models.Job


class JobCreateView(LoginRequiredMixin, CreateView):
    model = models.Job
    fields = ["company", "title", "currency", "hourly_rate"]
    success_url = reverse_lazy("job_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Job
    fields = ["company", "title", "currency", "hourly_rate"]
    success_url = "/"


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Job
    success_url = reverse_lazy("job_list")


class PeriodListView(LoginRequiredMixin, ListView):
    context_object_name = "periods"
    queryset = models.Period.objects.all().annotate(
        shifts=Count("shift"),
        hours=Sum("shift__length"),
        income=Sum("shift__length") * F("job__hourly_rate"),
    )


class PeriodShiftListView(LoginRequiredMixin, ListView):
    model = models.Shift
    context_object_name = "shifts"

    def get_queryset(self):
        return (
            super(PeriodShiftListView, self)
            .get_queryset()
            .filter(period=self.kwargs["pk"])
        )

    def get_context_data(self, *args, **kwargs):
        context = super(PeriodShiftListView, self).get_context_data(*args, **kwargs)
        return {
            **context,
            **models.Shift.objects.filter(period=self.kwargs["pk"]).aggregate(
                total_hours=Sum("length"),
                total_income=Sum("length") * F("period__job__hourly_rate"),
            ),
        }


class PeriodCreateView(LoginRequiredMixin, CreateView):
    model = models.Period
    fields = "__all__"
    success_url = reverse_lazy("period_list")


class PeriodUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Period
    fields = "__all__"
    success_url = reverse_lazy("period_list")


class PeriodDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Period
    success_url = reverse_lazy("period_list")


class ShiftListView(LoginRequiredMixin, ListView):
    model = models.Shift
    context_object_name = "shifts"

    def get_context_data(self, *args, **kwargs):
        context = super(ShiftListView, self).get_context_data(*args, **kwargs)
        return {
            **context,
            **models.Shift.objects.aggregate(
                total_hours=Sum("length"),
                total_income=Sum("length") * F("period__job__hourly_rate"),
            ),
        }


class ShiftCreateView(LoginRequiredMixin, CreateView):
    model = models.Shift
    fields = "__all__"
    success_url = reverse_lazy("shift_list")


class ShiftUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Shift
    fields = "__all__"
    success_url = reverse_lazy("shift_list")


class ShiftDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Shift
    success_url = reverse_lazy("shift_list")
