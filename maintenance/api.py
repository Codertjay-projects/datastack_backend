from helper import helper
from rest_framework.generics import ListAPIView, UpdateAPIView
from .serializers import MaintenanceSerializer
from .models import Maintenance


# Read Status
# get
# /v1/maintenance/read
class ReadMaintenanceStatus(ListAPIView):
    http_method_names = ["get"]

    def list(self, request):
        queryset = Maintenance.objects.all()

        return helper.createResponse(
            helper.message.MODULE_LIST("Maintenance"),
            MaintenanceSerializer(queryset, many=True).data,
        )


# Update API Status
# update
# /v1/maintenance/<str:id>
class UpdateMaintenanceStatus(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id=1):
        helper.checkParams(request, ["status", 'message'])
        api = helper.checkRecord(id, Maintenance, "Maintenance mode")

        api.status = helper.toBool(request.data["status"])
        api.message = request.data["message"]
        api.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("Maintenance mode", "updated")
        )
