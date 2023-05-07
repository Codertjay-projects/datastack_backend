from django.db import models
from subscription.models import Subscription
from account.models import User
import uuid


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subscription = models.ForeignKey(
        Subscription, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    duration = models.IntegerField()
    downloads = models.IntegerField(default=10)

    hosted_url = models.CharField(max_length=600, blank=True, null=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"
