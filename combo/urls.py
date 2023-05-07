from django.urls import path
from .api import (
    CreateCombo,
    ReadCombos,
    UpdateCombo,
    DeleteCombo,
)


# URLS
urlpatterns = [
    path("create", CreateCombo.as_view()),
    path("read", ReadCombos.as_view()),
    path("update/<str:id>", UpdateCombo.as_view()),
    path("delete/<str:id>", DeleteCombo.as_view()),
]
