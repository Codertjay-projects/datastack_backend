from django.db import models


# PrivacyPolicy MODEL
class PrivacyPolicy(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = "privacy_policy"
