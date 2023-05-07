from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView
)
from helper import helper
from .models import TOS
from .serializers import TOSSerilizer


# READ TOS
class ReadTOS(ListAPIView):
    http_method_names = ['get']

    def list(self, request):
        return helper.createResponse(
            helper.message.MODULE_LIST('TOS'),
            TOSSerilizer(
                TOS.objects.all(), many=True).data
        )


# UPDATE LINK
#  PUT
class UpdateTOS(UpdateAPIView):
    permission_classes = [
        helper.permission.IsAdmin
    ]

    def update(self, request, id):
        helper.checkParams(request, ['description'])

        try:
            tos = TOS.objects.get(id=id)
        except Exception:
            raise helper.exception.NotAcceptable(
                helper.message.MODULE_NOT_FOUND("TOS"))

        tos.description = request.data['description']
        tos.save()

        return helper.createResponse(helper.message.MODULE_STATUS_CHANGE('TOS', 'updated'))
