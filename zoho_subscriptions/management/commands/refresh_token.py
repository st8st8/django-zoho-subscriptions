from django.conf import settings
from django.core.management import BaseCommand

from zoho_subscriptions.client.client import Client


class Command(BaseCommand):
    args = ''
    help = 'Manually refreshes a Zoho access token, using the refresh token'

    def handle(self, *args, **options):
        self.client = Client(**settings.ZOHO_SUBSCRIPTION_CONFIG)
        self.client.refresh()