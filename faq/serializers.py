from rest_framework.serializers import ModelSerializer
from .models import FAQ


# FAQ Serializers
class FAQSerilizer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
