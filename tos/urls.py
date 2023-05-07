from django.urls import path
from .api import ReadTOS, UpdateTOS


urlpatterns = [
    # TOS PATHs
    path('read', ReadTOS.as_view()),
    path('update/<str:id>', UpdateTOS.as_view()),
]
