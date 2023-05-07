from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from helper import helper
from .models import Subscription
from .serializers import SubscriptionSerializer


# Create subscriptions
# post
# /v1/subscription/create
class Create(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]
    serializer_class = SubscriptionSerializer

    def create(self, request):
        helper.checkParams(
            request, ['name', 'price', 'duration', 'downloads'])
        body = request.data

        serializer = self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return helper.createResponse(
            helper.message.MODULE_STORE_SUCCESS('Subscription')
        )


# Read subscriptions
# get
# /v1/subscription/read
class Read(ListAPIView):
    def list(self, request):
        queryset = Subscription.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = helper.settings.PAGE_SIZE

        if 'filter' in request.GET:
            if helper.toBool(request.GET['filter']):
                queryset.filter(status=True)
            else:
                queryset.filter(status=False)

        page_context = paginator.paginate_queryset(
            queryset.order_by('-created'), request)

        return paginator.get_paginated_response(
            SubscriptionSerializer(page_context, many=True).data
        )


# Update subscriptions
# post
# /v1/subscription/update
class Update(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]
    serializer_class = SubscriptionSerializer

    def update(self, request, id):
        helper.checkParams(
            request, ['name', 'price', 'duration', 'downloads'])
        body = request.data

        subscription = helper.checkRecord(id, Subscription,  "Subscription")
        subscription.name = body['name']
        subscription.price = body['price']
        subscription.duration = body['duration']
        subscription.downloads = body['downloads']
        subscription.save()

        return helper.createResponse(
            helper.message.MODULE_STORE_SUCCESS('Subscription')
        )


# Delete subscriptions
# delete
# /v1/subscription/delete/<str:id>
class Delete(DestroyAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def delete(self, request, id):
        subcription = helper.checkRecord(id, Subscription, 'Subscription')
        subcription.delete()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('Subcription', 'deleted')
        )
