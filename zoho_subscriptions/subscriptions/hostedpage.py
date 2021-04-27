from zoho_subscriptions import models
from django.conf import settings as configuration
from zoho_subscriptions.client.client import Client


class HostedPage:
    def __init__(self, config=None):
        if config is None:
            self.client = Client(**configuration.ZOHO_SUBSCRIPTION_CONFIG)
        else:
            self.client = Client(config)

    def get_hostedpage_by_id(self, hostedpage_id):
        cache_key = 'zoho_customer_%s' % hostedpage_id
        response = self.client.get_from_cache(cache_key)
        if response is None:
            customer_by_hostedpage_id_uri = 'hostedpages/%s' % hostedpage_id
            result = self.client.send_request("GET", customer_by_hostedpage_id_uri)
            response = result
            zp = models.ZohoHostedPage.objects.get_or_create(
                zoho_id=hostedpage_id
            )
            zp.url = response["url"]
            zp.save()
            self.client.add_to_cache(cache_key, response)

    def create_hosted_page(self, user, plan_code, currency):
        data = {}
        if hasattr(user, "zoho_id"):
            data["customer_id"] = user.zoho_id
            data["currency_code"] = currency
        else:
            data["customer"] = {
                "display_name": user.get_full_name(),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "billing_address": {},
                "shipping_address": {},
                "currency_code": currency,
            }
        data.update({
            "plan": {
                "plan_code": plan_code
            }
        })

        response = self.client.send_request("POST", "hostedpages/newsubscription", data)
        response_data = response.json()
        if "hostedpage" in response_data:
            zp, created = models.ZohoHostedPage.objects.get_or_create(
                zoho_id=response_data["hostedpage"]["hostedpage_id"]
            )
            zp.raw = response.text
            zp.url = response_data["hostedpage"]["url"]
            zp.save()
        return response_data
