from django.db import models
from category.models import Category
import uuid


# Combo Model
class Combo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Combo details
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="combos")
    lines = models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # comobo release data
    releaseDate = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "combos"
