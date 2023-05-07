from django.urls import path
from .api import SellixWebhook


# URLS
urlpatterns = [
	path('sellix-webhook', SellixWebhook.as_view())
]
