from django.db import models


# Social Media  MODEL
class SocialMedia(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.URLField()

    class Meta:
        db_table = "social_media_links"
