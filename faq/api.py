from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from helper import helper
from .serializers import FAQSerilizer
from .models import FAQ


# Create FAQ
# post
# /v1/faq/create
class CreateFAQ(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]
    serializer_class = FAQSerilizer

    def post(self, request):
        helper.checkParams(request, ["question", "answer"])

        faq = self.get_serializer(data=request.data)
        faq.is_valid(raise_exception=True)
        faq.save()

        return helper.createResponse(helper.message.MODULE_STORE_SUCCESS("FAQ"))


# Read FAQ
# get
# /v1/faq/read
class ReadFAQs(ListAPIView):
    http_method_names = ["get"]

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST("FAQs"),
            FAQSerilizer(FAQ.objects.all(), many=True).data,
        )


# Update FAQ
# put
# /v1/faq/update/<str:id>
class UpdateFAQ(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id):
        helper.checkParams(request, ["question", "answer"])
        faq = helper.checkRecord(id, FAQ, "FAQ")

        faq.question = request.data["question"]
        faq.answer = request.data["answer"]
        faq.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("FAQ", "updated")
        )


# Delete FAQ
# delete
# /v1/faq/delete/<str:id>
class DeleteFAQ(DestroyAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def delete(self, request, id):
        faq = helper.checkRecord(id, FAQ, "FAQ")
        faq.delete()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("FAQ", "deleted")
        )
