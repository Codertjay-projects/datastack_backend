from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Invoice


class InvoiceSerializer(ModelSerializer):
    username = SerializerMethodField("getUsername")
    userEmail = SerializerMethodField("getEmail")
    userId = SerializerMethodField("getId")

    class Meta:
        model = Invoice
        exclude = ["user"]

    def getUsername(self, obj):
        return obj.user.username

    def getEmail(self, obj):
        return obj.user.email

    def getId(self, obj):
        return obj.user.id
