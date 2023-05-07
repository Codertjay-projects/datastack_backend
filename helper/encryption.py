from cryptography.fernet import Fernet
from django.conf import settings
import json


ENC_KEY = settings.ENC_KEY


def encrypt(json_data):
    print(json_data)
    string = str.encode(json.dumps(json_data))
    f = Fernet(ENC_KEY)
    return f.encrypt(string).decode()


def decrypt(string):
    f = Fernet(ENC_KEY)
    return json.loads(f.decrypt(str.encode(string)))
