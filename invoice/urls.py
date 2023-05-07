from django.urls import path
from .api import CreateInvoice, ReadInvoices, ReadInvoice


urlpatterns = [
    path("create", CreateInvoice.as_view()),
    path("read", ReadInvoices.as_view()),
    path("read/<str:id>", ReadInvoice.as_view()),
]
