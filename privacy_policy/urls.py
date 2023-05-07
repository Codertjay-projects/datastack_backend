from django.urls import path
from .api import ReadPrivacyPolicy, UpdatePrivacyPolicy


urlpatterns = [
    path('read', ReadPrivacyPolicy.as_view()),
    path('update/<str:id>', UpdatePrivacyPolicy.as_view()),
]
