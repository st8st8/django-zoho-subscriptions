from django.test import TestCase
from zoho_subscriptions.subscriptions.subscription import Subscription


class SubscriptionTest(TestCase):
    def get_list(self):
        subscriptions = Subscription()
        print(subscriptions.list_subscriptions_by_customer("112407000000035015"))

    def get_details(self):
        subscriptions = Subscription()
        print(subscriptions.get_subscriptions("112407000000238188"))

