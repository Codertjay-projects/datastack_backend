from django.db import models

# FAQs Model
class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=800)
    answer = models.TextField()

    class Meta:
        db_table = "faqs"
