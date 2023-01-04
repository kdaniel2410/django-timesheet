from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'jobs', views.JobViewSet)
router.register(r'periods', views.PeriodViewSet)
router.register(r'shifts', views.ShiftViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
