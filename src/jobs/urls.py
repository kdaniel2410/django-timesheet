from . import views
from django.urls import path

urlpatterns = [
    path("", views.JobTableView.as_view(), name="job_table"),
    path("jobs/create/", views.JobCreateView.as_view(), name="job_create"),
    path("jobs/<int:pk>/update/", views.JobUpdateView.as_view(), name="job_update"),
    path("jobs/<int:pk>/delete/", views.JobDeleteView.as_view(), name="job_delete"),

    path("jobs/<int:job_pk>/periods/", views.PeriodListView.as_view(), name="period_list"),
    path("jobs/<int:job_pk>/periods/table/", views.PeriodTableView.as_view(), name="period_table"),
    path("jobs/<int:job_pk>/periods/create/", views.PeriodCreateView.as_view(), name="period_create"),
    path("periods/<int:pk>/update/", views.PeriodUpdateView.as_view(), name="period_update"),
    path("periods/<int:pk>/delete/", views.PeriodDeleteView.as_view(), name="period_delete"),

    path("jobs/<int:job_pk>/periods/<int:period_pk>/shifts/", views.ShiftListView.as_view(), name="shift_list"),
    path("jobs/<int:job_pk>/periods/<int:period_pk>/shifts/table/", views.ShiftTableView.as_view(), name="shift_table"),
    path("jobs/<int:job_pk>/periods/<int:period_pk>/shifts/create/", views.ShiftCreateView.as_view(), name="shift_create"),
    path("jobs/<int:job_pk>/periods/<int:period_pk>/shifts/create/length/", views.ShiftCreateViewAlt.as_view(), name="shift_create_alt"),
    path("shifts/<int:pk>/update/", views.ShiftUpdateView.as_view(), name="shift_update"),
    path("shifts/<int:pk>/update/length/", views.ShiftUpdateViewAlt.as_view(), name="shift_update_alt"),
    path("shifts/<int:pk>/delete/", views.ShiftDeleteView.as_view(), name="shift_delete"),
]
