from django.urls import path
from .api import CreateCategory, ReadCategory, UpdateCategory, DeleteCategory


# URLS
urlpatterns = [
    path("create", CreateCategory.as_view()),
    path("read", ReadCategory.as_view()),
    path("update/<str:id>", UpdateCategory.as_view()),
    path("delete/<str:id>", DeleteCategory.as_view()),
]
