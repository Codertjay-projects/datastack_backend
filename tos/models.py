from django.db import models


# TOS MODEL
class TOS(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = "terms_of_service"
