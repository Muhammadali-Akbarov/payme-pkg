from django.urls import path

from payme.views import PaymeWebHookAPIView


urlpatterns = [
    path("update/", PaymeWebHookAPIView.as_view())
]
