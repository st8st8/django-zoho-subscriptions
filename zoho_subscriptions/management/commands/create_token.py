from django.conf import settings
from django.core.management import BaseCommand

from zoho_subscriptions.client.client import Client


class Command(BaseCommand):
    args = ''
    help = 'Helper to create a new refresh and access token for Zoho API'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('code', type=str,
                            help="The code returned from the first step (https://www.zoho.com/subscriptions/api/v1/)")

    def handle(self, *args, **options):
        self.client = Client(**settings.ZOHO_SUBSCRIPTION_CONFIG)
        self.client.begin(options["code"])