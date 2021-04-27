import json
from datetime import timedelta

import requests
from cachetools import TTLCache
from django.utils import timezone

from zoho_subscriptions.utils.constants import DEFAULT_CACHE_MODE, DEFAULT_CACHE_TTL, ZOHO_AUTH_HEADER, ZOHO_AUTH_TOKEN_HEADER_PREFIX, \
    ZOHO_ORG_ID_HEADER, DEFAULT_CACHE_MAXSIZE
from zoho_subscriptions import models


class Client:
    def __init__(self, api_url='https://subscriptions.zoho.eu/api/v1/',
                 account_url="https://accounts.zoho.eu/oauth/v2/",
                 access_token=None,
                 client_id=None, client_secret=None, refresh_token=None, redirect_uri=None,
                 zoho_org_id=None, cache_enabled=True, cache_ttl=600, debug=True, **kwargs):
        self.api_url = api_url
        self.account_url = account_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.redirect_uri = redirect_uri
        self.zoho_org_id = zoho_org_id
        self.debug = debug
        try:
            self.cache_enabled = cache_enabled
        except KeyError:
            self.cache_enabled = DEFAULT_CACHE_MODE

        try:
            self.cache_ttl = cache_ttl
        except KeyError:
            self.cache_ttl = DEFAULT_CACHE_TTL
        self.requests = requests.Session()
        self.cache = TTLCache(ttl=self.cache_ttl, maxsize=DEFAULT_CACHE_MAXSIZE)

    def get_access_token(self):
        if self.access_token:
            return self.access_token
        try:
            access_token = models.AccessToken.objects.get(expiry_date__gt=timezone.now()).access_token
        except models.AccessToken.DoesNotExist:
            refresh_data = self.refresh()
            access_token = refresh_data["access_token"]
        return access_token

    def begin(self, code):
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        response_body = None
        try:
            response = requests.request("POST", self.account_url + "token", data=data)
            response_body = response.content
            response_data = response.json()
            print(response_data)
        finally:
            models.ZohoLog.objects.create(
                request=json.dumps(data),
                response=response_body
            )

        return response_data

    def refresh(self):
        data = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "refresh_token",
        }
        response_body = None
        try:
            response = requests.request("POST", self.account_url + "token", data=data)
            response_body = response.content
            response_data = response.json()
            print(response_data)
            models.AccessToken.objects.create(
                access_token=response_data["access_token"],
                expiry_date=timezone.now() + timedelta(seconds=response_data["expires_in"])
            )
        finally:
            models.ZohoLog.objects.create(
                request=json.dumps(data),
                response=response_body
            )

        return response_data

    def add_to_cache(self, key, value):
        if (self.cache_enabled is None) or (self.cache_enabled is False):
            pass
        else:
            self.cache[key] = value

    def get_from_cache(self, key):
        if (self.cache_enabled is None) or (self.cache_enabled is False):
            return None
        else:
            try:
                return self.cache[key]
            except KeyError:
                return None

    def delete_from_cache(self, key):
        if (self.cache_enabled is None) or (self.cache_enabled is False):
            return False
        else:
            try:
                self.cache.pop(key=key)
                return True
            except KeyError:
                return False
            # my_key = ast.literal_eval(key)
            # return self.cache.pop(key=key)

    def get_request_headers(self, headers):
        access_token = self.get_access_token()
        default_headers = {
            ZOHO_AUTH_HEADER: ZOHO_AUTH_TOKEN_HEADER_PREFIX + access_token,
            ZOHO_ORG_ID_HEADER: self.zoho_org_id,
            'Content-Type': "application/json"
        }
        if (headers is not None) and len(headers) > 0:
            default_headers.update(headers)
        return default_headers

    def send_request(self, method, uri, data=None, headers=None):

        headers = self.get_request_headers(headers)
        url = self.api_url + uri
        if True:
            print("Method: {0}".format(method))
            print("url: {0}".format(url))
            print("headers: {0}".format(json.dumps(headers)))
            print("data: {0}".format(json.dumps(data)))
        response = requests.request(method, self.api_url + uri, data=json.dumps(data),
                                    headers=headers)
        # response.raise_for_status()
        return response

