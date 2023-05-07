from django.db import models
import uuid


class Maintenance(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    message = models.TextField(default="")

    class Meta:
        db_table = "site_maintenance"
