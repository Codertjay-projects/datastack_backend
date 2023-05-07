from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
import random
import string
import requests
import os
from . import encryption, exception, mail, message, permission, request, payment
import json
from datetime import datetime, timedelta


# Generate OTP
def generateOTP(length):
    length -= 1
    return random.randint(int("1" + "0" * length), int("9" + "9" * length))


# Check for parameters in requests
def checkParams(request, params):
    if not all(param in request.data for param in params):
        raise exception.NotAcceptable(message.NOT_VALID_PARAMS)
    return True


# Custom Response for API
def createResponse(message="", payload={}, status_code=200):
    return Response({"detail": message, "payload": payload}, status=status_code)


# Generate JWT token for user
def get_token(user):
    return api_settings.JWT_ENCODE_HANDLER(api_settings.JWT_PAYLOAD_HANDLER(user))


# is record found
# id = record id, model=Record model, attribute = for message
def checkRecord(id, model, attribute):
    try:
        record = model.objects.get(id=id)
    except Exception:
        raise exception.NotAcceptable(message.MODULE_NOT_FOUND(attribute))
    return record


# Check if text is True or False from true / false
def toBool(v):
    v = str(v)
    return v.lower() in ("yes", "true", "t", "1")


# Check id input Is Empty
def isEmpty(var, name):
    if not var:
        raise exception.NotAcceptable(message.INVALID_INPUT(name))


# generate random string
def randomString(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(length))


# Verify Google reCaptcha
def verify_recaptcha(request, RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY):
    return True
    checkParams(request, ["g-recaptcha-response"])
    status = (
        requests.post(
            settings.GOOGLE_VERIFY_RECAPTCHA_URL,
            data={
                "secret": RECAPTCHA_SECRET_KEY,
                "response": request.data["g-recaptcha-response"],
            },
            verify=True,
        )
        .json()
        .get("success", False)
    )

    if not status:
        raise exception.ParseError(message.INVALID_RECAPTCHA)

    return status


# Get user up
def get_client_ip(request):
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    print(request.data)
    ip = str(request.data['ip'])
    response = requests.get(
        "https://geolocation-db.com/json/"+ip+"&position=true").json()
    print(response)
    return ip, response['city']


# Generate Key Helper Fucntions
def key(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generateKey(price):
    code = 'DS-'+key()+'-'+key()+'-'+key()+'-'+str(price)
    return code


def comboDownloadLimit(user, UserSubscriptions):
    try:
        subscription = UserSubscriptions.objects.filter(
            user=user, expiry__gte=datetime.now())
        return subscription.subscription.downloads
    except Exception:
        return settings.COMBO_DOWNLOAD_LIMIT


def genSecretKey():
    secret_pass = ''.join(random.choice(
        string.ascii_lowercase)for _ in range(6))
    secret_key = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(8))+''+str(random.randint(10, 100))+'@gmail.com:'+secret_pass

    return secret_key
