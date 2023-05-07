from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from helper import helper
from subscription.models import Subscription
from .models import Invoice
from .serializers import InvoiceSerializer
from django.db.models import Q


# Create Invoice
# post
# /v1/invoice/create
class CreateInvoice(CreateAPIView):
    permission_classes = [helper.permission.IsAuthenticated]

    def post(self, request):
        helper.checkParams(request, ['subscription'])
        body = request.data
        user = request.user

        subscription = helper.checkRecord(
            body['subscription'], Subscription, 'Subscription')

        price = subscription.price

        invoice = Invoice.objects.create(
            user=user,
            price=price,
            duration=subscription.duration,
            subscription=subscription,
            downloads=subscription.downloads,
            name=subscription.name
        )

        data = {
            "amount": price,
            "invoice_id": str(invoice.id),
            "metadata": {
                "token": helper.encryption.encrypt({"invoice": str(invoice.id)})
            }
        }

        rsp = helper.payment.sellix_api(user.email, price, data)

        invoice.hosted_url = rsp['data']['url']
        invoice.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("Invoice", "created"),
            {"url": invoice.hosted_url},
        )


# Read Invoices
# get
# /v1/invoice/read
class ReadInvoices(ListAPIView):
    permission_classes = [helper.permission.IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = helper.settings.PAGE_SIZE
        queryset = Invoice.objects.all()

        if request.user.is_superuser:
            if 'search' in request.GET:
                search = request.GET['search']
                queryset = queryset.filter(Q(user__username__icontains=search) | Q(
                    user__email__icontains=search) | Q(hosted_url__icontains=search))
        else:
            queryset.filter(user=request.user)

        page_context = paginator.paginate_queryset(queryset, request)

        return paginator.get_paginated_response(
            InvoiceSerializer(page_context, many=True).data
        )


# Read Single Invoice
# get
# /v1/invoice/read/<str:id>
class ReadInvoice(ListAPIView):
    permission_classes = [helper.permission.IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request, id):
        invoice = helper.checkRecord(id, Invoice, 'Invoice')

        if invoice.user != request.user:
            raise helper.exception.ParseError(
                helper.message.MODULE_NOT_FOUND('Invoice'))

        return helper.createResponse(
            helper.message.MODULE_LIST('Invoice'),
            {
                "invoice": InvoiceSerializer(invoice).data
            }
        )
