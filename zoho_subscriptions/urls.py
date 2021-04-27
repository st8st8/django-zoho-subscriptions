from django.urls import path

from zoho_subscriptions import views

app_name = "zoho_subscriptions"

urlpatterns = [
    path("new-subscription/<slug:upc>/<str:currency>", views.NewSubscriptionView.as_view())
]
