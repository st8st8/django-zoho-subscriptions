from django.contrib.auth.models import User
from django.test import TestCase

from zoho_subscriptions.subscriptions.hostedpage import HostedPage
from zoho_subscriptions.subscriptions.subscription import Subscription


class HostedPageTest(TestCase):
    def new_page_existing_customer(self):
        hostedpages = HostedPage()
        user = User.objects.create(
            first_name="James",
            last_name="Tweed",
            email="jtweed@coracleonline.com"
        )
        user.zoho_id = "112407000000032678"
        res = hostedpages.create_hosted_page(user, "coracle-mathsatseaplus", "USD")
        print(res)

    def new_page_new_customer(self):
        hostedpages = HostedPage()
        user = User.objects.create(
            first_name="Test",
            last_name="Testshaw",
            email="test-steve1@mycoracle.com"
        )
        res = hostedpages.create_hosted_page(user, "coracle-mathsatseaplus", "USD")
        print(res)

