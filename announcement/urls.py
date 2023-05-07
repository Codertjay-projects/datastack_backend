from django.urls import path
from .api import ReadAnnouncement, UpdateAnnouncement


urlpatterns = [
    path("read", ReadAnnouncement.as_view()),
    path("update/<str:id>", UpdateAnnouncement.as_view()),
]