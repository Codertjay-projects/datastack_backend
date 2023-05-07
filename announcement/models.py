from django.db import models
import uuid


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=400)
    status = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "announcement"