from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView
)
from helper import helper
from .models import PrivacyPolicy
from .serializers import PrivacyPolicySerilizer


# READ PrivacyPolicy
class ReadPrivacyPolicy(ListAPIView):
    http_method_names = ['get']

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST('PrivacyPolicy'),
            PrivacyPolicySerilizer(
                PrivacyPolicy.objects.all(), many=True).data
        )


# UPDATE LINK
#  PUT
class UpdatePrivacyPolicy(UpdateAPIView):
    permission_classes = [
        helper.permission.IsAdmin
    ]

    def update(self, request, id):
        helper.checkParams(request, ['description'])

        try:
            privacy_policy = PrivacyPolicy.objects.get(id=id)
        except Exception:
            raise helper.exception.NotAcceptable(
                helper.message.MODULE_NOT_FOUND("PrivacyPolicy"))

        privacy_policy.description = request.data['description']
        privacy_policy.save()

        return helper.createResponse(helper.message.MODULE_STATUS_CHANGE('PrivacyPolicy', 'updated'))
