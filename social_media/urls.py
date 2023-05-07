from django.urls import path
from .api import ReadLinks, UpdateLink

urlpatterns = [
    path("read", ReadLinks.as_view()),
    path("update/<str:id>", UpdateLink.as_view()),
]
