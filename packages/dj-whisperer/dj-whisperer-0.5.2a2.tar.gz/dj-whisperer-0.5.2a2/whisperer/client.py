import hashlib
import hmac
import json

import requests
from requests.auth import HTTPBasicAuth
from rest_framework.utils.encoders import JSONEncoder

from whisperer.conf import settings


class WebhookClient(object):
    def __init__(self, event_type, payload):
        self.event_type = event_type
        self.payload = payload
        self.headers = {
            'Content-Type': 'application/json',
            'X-Whisperer-Event': self.event_type,
        }

    def sign(self, secret_key, payload):
        signature = hmac.new(
            secret_key.encode('utf-8'),
            payload.encode('utf-8'),
            digestmod=hashlib.sha256,
        )
        self.headers['X-Whisperer-Signature'] = 'sha256={}'.format(
            signature.hexdigest()
        )

    def send_payload(
        self,
        target_url,
        payload,
        secret_key=None,
        additional_headers=None,
        auth_config=None,
        *args,
        **kwargs
    ):
        payload = json.dumps(payload, cls=JSONEncoder)
        auth = None
        if secret_key:
            self.sign(secret_key, payload)
        if auth_config:
            auth = self._get_auth(auth_config)
        if additional_headers:
            self.headers.update(additional_headers)
        response = requests.post(
            url=target_url,
            data=payload,
            headers=self.headers,
            timeout=settings.WHISPERER_REQUEST_TIMEOUT,
            auth=auth,
        )
        return response

    def _get_auth(self, auth_config):
        if auth_config.get('auth_type') == 'basic':
            username = auth_config.get('username')
            password = auth_config.get('password')
            return HTTPBasicAuth(username, password)
