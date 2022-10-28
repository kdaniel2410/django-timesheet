from . import views
from django.urls import path

urlpatterns = [
    path("", views.JobListView.as_view(), name="job_list"),
    path("jobs/create/", views.JobCreateView.as_view(), name="job_create"),
    path("jobs/<int:pk>/update/", views.JobUpdateView.as_view(), name="job_update"),
    path("jobs/<int:pk>/delete/", views.JobDeleteView.as_view(), name="job_delete"),
    path("periods", views.PeriodListView.as_view(), name="period_list"),
    path("periods/<int:pk>/shifts", views.PeriodShiftListView.as_view(), name="period_shift_list"),
    path("periods/create/", views.PeriodCreateView.as_view(), name="period_create"),
    path("periods/<int:pk>/update/", views.PeriodUpdateView.as_view(), name="period_update"),
    path("periods/<int:pk>/delete/", views.PeriodDeleteView.as_view(), name="period_delete"),
    path("shifts/", views.ShiftListView.as_view(), name="shift_list"),
    path("shifts/create/", views.ShiftCreateView.as_view(), name="shift_create"),
    path("shifts/<int:pk>/update/", views.ShiftUpdateView.as_view(), name="shift_update"),
    path("shifts/<int:pk>/delete/", views.ShiftDeleteView.as_view(), name="shift_delete"),
]
