from rest_framework.generics import ListAPIView, UpdateAPIView
from helper import helper
from .models import SocialMedia
from .serializers import SocialMediaSerilizer


# Read Social Media Links
# get
# /v1/faq/create
class ReadLinks(ListAPIView):
    http_method_names = ["get"]

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST("Social media links"),
            SocialMediaSerilizer(SocialMedia.objects.all(), many=True).data,
        )


# Update Social Media Links
# put
# /v1/faq/update/<str:id>
class UpdateLink(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id):
        helper.checkParams(request, ['url'])
        link = helper.checkRecord(id, SocialMedia, "Social media link")

        link.url = request.data["url"]
        link.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("Social media link", "updated")
        )
