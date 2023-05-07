from rest_framework.serializers import ModelSerializer
from .models import Announcement


class AnnouncementSerializer(ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"
