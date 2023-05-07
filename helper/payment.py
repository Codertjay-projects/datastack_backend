from django.conf import settings
import requests
import json


# Sellix Payment Gateway
def sellix_api(email, amount, metadata):
    print(email, amount, metadata)
    headers = {
        "Authorization": "Bearer " + settings.SELLIX_KEY
    }
    params = {
        "title": "License Purchase",
        "gateway": ["PAYPAL", "STRIPE", "CRYPTO"],
        "value": amount,
        "currency": "USD",
        "confirmations": 1,
        "email": email,
        "custom_fields":  metadata,
        "webhook": "https://api.stacked.to/v1/webhook/sellix-webhook",
        "white_label": False,
        "return_url": "https://stacked.to"
    }
    response = requests.post(
        'https://dev.sellix.io/v1/payments', data=json.dumps(params), headers=headers)

    return response.json()
