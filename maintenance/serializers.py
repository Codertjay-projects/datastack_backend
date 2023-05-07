from rest_framework.serializers import ModelSerializer
from .models import Maintenance


class MaintenanceSerializer(ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"