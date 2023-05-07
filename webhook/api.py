from rest_framework.generics import CreateAPIView
from users.models import UserSubscriptions
from invoice.models import Invoice
from subscription.models import Subscription
from helper import helper


# Sellix Webhook
# post
# /v1/webhook/sellix
class SellixWebhook(CreateAPIView):
    def post(self, request):
        request_data = request.data

        for i in range(0, len(request_data['data']['status_history'])):
            print(request_data['data']['status_history']
                  [i]['status'])

            if request_data['data']['status_history'][i]['status'] == "COMPLETED":
                metadata = request_data['data']['custom_fields']

                invoice = helper.checkRecord(
                    metadata['invoice_id'], Invoice, "Invoice")

                if not invoice.status:
                    invoice.status = True
                    userSubscription = UserSubscriptions.objects.create(
                        user=invoice.user,
                        subscription=invoice.subscription,
                        expiry=helper.timezone.now() + helper.timedelta(invoice.subscription.duration)
                    )
                    userSubscription.save()
                    invoice.save()
                    return helper.createResponse(
                        helper.message.ORDER_ALREADY_FULLFILLED,
                    )

                break

        return helper.createResponse(
            helper.message.PENDING_WEBHOOK,
            {},
            400
        )
