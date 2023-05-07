from django.urls import path
from .api import CreateFAQ, ReadFAQs, UpdateFAQ, DeleteFAQ


urlpatterns = [
    path("create", CreateFAQ.as_view()),
    path("read", ReadFAQs.as_view()),
    path("update/<str:id>", UpdateFAQ.as_view()),
    path("delete/<str:id>", DeleteFAQ.as_view()),
]