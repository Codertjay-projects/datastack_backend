from decimal import Context
import re
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from helper import helper
from category.models import Category
from users.models import DownloadedCombo
from .serializers import ComboSerializer, ReadComboSerializer, AdminComboSerializer
from .models import Combo


def releaseCombos():
    queryset = Combo.objects.filter(releaseDate__lte=helper.datetime.now())
    for combo in queryset:
        combo.status = True
        combo.created = combo.releaseDate
        combo.releaseDate = None
        combo.save()

    return


# Create Combo
# post
# /v1/combo/create
class CreateCombo(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]
    serializer_class = ComboSerializer

    def create(self, request):
        helper.checkParams(request, ['combo', 'name', 'category'])
        helper.checkRecord(request.data['category'], Category, "Category")

        body = request.data

        data = {}
        data['name'] = body['name']
        data['lines'] = sum(1 for line in request.FILES['combo'].readlines())
        data['file'] = request.FILES['combo']
        data['category'] = body['category']

        if "releaseDate" in body:
            if body['releaseDate']:
                data['releaseDate'] = body['releaseDate']
                data['status'] = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return helper.createResponse(
            helper.message.MODULE_STORE_SUCCESS('Combo')
        )


# Read Comobos
# get
# /v1/combo/read
class ReadCombos(ListAPIView):
    permission_classes = [helper.permission.IsAuthenticated]

    def list(self, request):
        releaseCombos()
        queryset = Combo.objects.filter()

        paginator = PageNumberPagination()
        paginator.page_size = helper.settings.PAGE_SIZE

        if "search" in request.GET:
            if request.GET['search']:
                queryset = queryset.exclude(
                    ~Q(name__icontains=request.GET['search']))

        if "category" in request.GET:
            if request.GET['category']:
                queryset = queryset.exclude(
                    ~Q(category__name=request.GET['category']))

        if 'downloaded' in request.GET:
            if request.GET['downloaded']:
                queryset = queryset.exclude(id__in=DownloadedCombo.objects.filter(
                    user=request.user).values_list('combo', flat=True))

        if 'date' in request.GET:
            if request.GET['date']:
                queryset = queryset.exclude(~Q(created__gte=helper.datetime.now(
                ) - helper.timedelta(days=int(request.GET['date']))))

        # full details for admin
        if request.user.is_superuser:
            page_context = paginator.paginate_queryset(
                queryset.order_by('-created'), request)
            return paginator.get_paginated_response(
                AdminComboSerializer(page_context, many=True).data
            )
        queryset = queryset.filter(status=True)
        page_context = paginator.paginate_queryset(
            queryset.order_by('-created'), request)

        return paginator.get_paginated_response(
            ReadComboSerializer(page_context, context=request, many=True).data
        )


# Update Combo Category
# put
# /v1/combo/update/<str:id>
class UpdateCombo(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id):
        helper.checkParams(request, ['name', 'category'])
        body = request.data

        combo = helper.checkRecord(id, Combo, "Combo")
        category = helper.checkRecord(body['category'], Category, "Category")

        combo.name = body['name']
        combo.category = category
        combo.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('Combo', 'updated'),
        )


# Delete Combo
# delete
# /v1/comobo/delete
class DeleteCombo(DestroyAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def delete(self, request, id):
        combo = helper.checkRecord(id, Combo, 'Combo')
        combo.delete()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('Combo', 'deleted')
        )
