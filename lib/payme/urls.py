from django.urls import path

from payme.views import MerchantAPIView


urlpatterns = [
    path("merchant/", MerchantAPIView.as_view())
]
