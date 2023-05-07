from django.urls import path
from .api import Create, Read, Update, Delete


# URLS
urlpatterns = [
    path("create", Create.as_view()),
    path("read", Read.as_view()),
    path("update/<str:id>", Update.as_view()),
    path("delete/<str:id>", Delete.as_view()),
]
