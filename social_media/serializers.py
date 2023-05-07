from rest_framework.serializers import ModelSerializer
from .models import SocialMedia


# Social Media
class SocialMediaSerilizer(ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"
