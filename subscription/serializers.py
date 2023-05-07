from rest_framework.serializers import ModelSerializer
from .models import Subscription


# Subscription Serializer
class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
