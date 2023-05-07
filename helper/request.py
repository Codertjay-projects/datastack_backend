import requests
import json


def get(url, headers={'content-type': "application/json"}, params={}):
    return requests.get(url, data=params, headers=headers)


def post(url, headers={'content-type': "application/json"}, params={}):
    return requests.post(url, data=json.dumps(params), headers=headers)
