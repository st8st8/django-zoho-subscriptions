from django.contrib import admin
from django.contrib.admin import register
from zoho_subscriptions import models


@register(models.AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ["access_token", "expiry_date"]
    ordering = ["expiry_date"]


@register(models.ZohoHostedPage)
class ZohoHostedPageAdmin(admin.ModelAdmin):
    list_display = ["zoho_id", "url"]
    search_fields = ["zoho_id", "url"]
    ordering = ["zoho_id"]


@register(models.ZohoLog)
class ZohoLogAdmin(admin.ModelAdmin):
    list_display = ["created_date", "request"]
    search_fields = ["request"]
    ordering = ["created_date"]
