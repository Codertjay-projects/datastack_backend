from django.db import models
import uuid


# License Keys
class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    duration = models.IntegerField(default=30)
    price = models.FloatField(default=0)
    downloads = models.IntegerField(default=0)
    status = models.BooleanField(default=1)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subscriptions"
