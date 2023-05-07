from helper import helper
from .serializezrs import AnnouncementSerializer
from .models import Announcement
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
)


# Read Announcement
# get
# /v1/announcement/read
class ReadAnnouncement(ListAPIView):
    http_method_names = ["get"]

    def list(self, request):
        queryset = Announcement.objects.all()

        return helper.createResponse(
            helper.message.MODULE_LIST("Announcement"),
            AnnouncementSerializer(queryset, many=True).data,
        )


# Update Announcement
# put
# /v1/announcement/update/<str:id>
class UpdateAnnouncement(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id):
        helper.checkParams(request, ["title", "status"])
        announcement = helper.checkRecord(id, Announcement, "Announcement")

        announcement.title = request.data["title"]
        announcement.status = helper.toBool(request.data["status"])
        announcement.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("Announcement", "updated")
        )
