from django.urls import path
from .api import ReadMaintenanceStatus, UpdateMaintenanceStatus


urlpatterns = [
    path("read", ReadMaintenanceStatus.as_view()),
    path("update/<str:id>", UpdateMaintenanceStatus.as_view()),
]