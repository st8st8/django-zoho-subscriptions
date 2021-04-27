from django.db import models


class AccessToken(models.Model):
    access_token = models.TextField()
    expiry_date = models.DateTimeField()

    def __str__(self):
        return self.access_token


class ZohoHostedPage(models.Model):
    zoho_id = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    raw = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.zoho_id


class ZohoLog(models.Model):
    request = models.TextField()
    response = models.TextField(null=True, blank=True,
                           help_text="The raw response, from Zoho")
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}".format(self.request)