from django.db import models
from account.models import User
from combo.models import Combo
from category.models import Category
from subscription.models import Subscription
import uuid


# License Keys
class DownloadedCombo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    downlaoded = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "download_list"


# Purchase History
class UserSubscriptions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    expiry = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_subscriptions"
