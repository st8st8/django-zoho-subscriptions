import ast
from requests import HTTPError

from zoho_subscriptions.client.client import Client
from zoho_subscriptions.subscriptions.addon import Addon
from zoho_subscriptions.subscriptions.customer import Customer
from zoho_subscriptions.subscriptions.hostedpage import HostedPage
from zoho_subscriptions.subscriptions.invoice import Invoice
from zoho_subscriptions.subscriptions.plan import Plan
from django.conf import settings as configuration


class Subscription:

    def __init__(self, config=None):
        if config is None:
            self.client = Client(**configuration.ZOHO_SUBSCRIPTION_CONFIG)
        else:
            self.client = Client(config)

    def plan(self):
        return Plan(self.client)

    def customer(self):
        return Customer(self.client)

    def add_on(self):
        return Addon(self.client)

    def invoice(self):
        return Invoice(self.client)

    def hosted_page(self):
        return HostedPage(self.client)

    def get(self, id):
        cache_key = "zoho_subscription_%s" % id
        response = self.client.get_from_cache(cache_key)
        if response is None:
            get_subscription_by_id_uri = "subscriptions/%s" % id
            response = self.client.send_request("GET", get_subscription_by_id_uri)
            self.client.add_to_cache(cache_key, response)
        else:
            print ("Returning from cache : " + cache_key)
        return response

    def create(self, data):
        return self.client.send_request("POST", 'subscriptions', data=data, headers=None)

    def cancel_at_end(self, subscription_id):
        return self.client.send_request("POST", 'subscriptions/{0}/cancel?cancel_at_end=true'.format(subscription_id), headers=None)

    def buy_add_on(self, subscription_id, data):
        buy_add_on_uri = 'subscriptions/%s/buyonetimeaddon' % subscription_id
        return self.client.send_request("POST", buy_add_on_uri, data=data, headers=None)

    def associate_coupon(self, subscription_id, coupon_code):
        coupon_uri = 'subscriptions/%s/coupons/%s' % (subscription_id, coupon_code)
        return self.client.send_request("POST", coupon_uri)

    def reactivate(self, subscription_id):
        reactivate_uri = 'subscriptions/%s/reactivate' % subscription_id
        self.client.send_request("POST", reactivate_uri)

    def list_subscriptions_by_customer(self, customer_id):
        cache_key = "zoho_subscriptions_by_customer_%s" % customer_id
        response = self.client.get_from_cache(cache_key)
        if response is None:
            subscriptions_by_customer_uri = 'subscriptions?customer_id=%s' % customer_id
            result = self.client.send_request("GET", subscriptions_by_customer_uri)
            if isinstance(result, HTTPError):
                raise HTTPError(result)
            response = result['subscriptions']
            self.client.add_to_cache(cache_key, response)
        else:
            print("Returning from cache : " + cache_key)
        return response

    def get_subscriptions(self,subscription_id):
        cache_key = "zoho_subscriptions_by_customer_%s" % subscription_id
        response = self.client.get_from_cache(cache_key)
        if response is None:
            subscriptions_by_subscription_id_uri = 'subscriptions/%s'%subscription_id
            result = self.client.send_request("GET", subscriptions_by_subscription_id_uri)
            if type(result) is HTTPError:
                result_bytes = result.response._content
                result_dict = ast.literal_eval(result_bytes.decode('utf-8'))
                return result_dict['message']
            else:
                response = result['subscription']
                self.client.add_to_cache(cache_key, response)
        else:
            print("Returning from cache : " + cache_key)
        return response




