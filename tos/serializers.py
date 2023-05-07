from rest_framework.serializers import ModelSerializer
from .models import TOS


# TOS SERIALIZER
class TOSSerilizer(ModelSerializer):
    class Meta:
        model = TOS
        fields = "__all__"
