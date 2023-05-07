from rest_framework.serializers import ModelSerializer
from .models import PrivacyPolicy


# PrivacyPolicy SERIALIZER
class PrivacyPolicySerilizer(ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"
