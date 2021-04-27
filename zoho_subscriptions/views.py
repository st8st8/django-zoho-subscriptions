import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import RedirectView
from oscar.apps.catalogue.models import Product

from zoho_subscriptions.subscriptions.hostedpage import HostedPage


class NewSubscriptionView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if kwargs["currency"] not in settings.ZOHO_CURRENCIES:
            raise Http404
        product = get_object_or_404(
            Product,
            upc=kwargs["upc"]
        )

        hostedpage = HostedPage()
        response = hostedpage.create_hosted_page(self.request.user, product.attr.zoho_plan_code, kwargs["currency"])
        if "hostedpage" in response:
            return response["hostedpage"]["url"]
        else:
            messages.error(self.request, "There was a problem loading the payment page: {0}".format(response["message"]))
            logging.getLogger().error("Error loading zoho payment page:")
            logging.getLogger().error(json.dumps(response))
            return "/"

