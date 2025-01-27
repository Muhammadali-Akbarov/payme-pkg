<h1 align="center">Payme Software Development Kit</h1>

<p align="center">
  <a href="https://t.me/+lO97J78xBj45MzBi">
    <img src="https://img.shields.io/badge/Support%20Group-blue?logo=telegram&logoColor=white" alt="Support Group on Telegram"/>
  </a>
</p>

<p align="center">
  <a href="https://docs.pay-tech.uz"><img src="https://img.shields.io/static/v1?message=Documentation&logo=gitbook&logoColor=ffffff&label=%20&labelColor=5c5c5c&color=3F89A1"></a>
  <a href="https://github.com/PayTechUz/payme-pkg"><img src="https://img.shields.io/badge/Open_Source-❤️-FDA599?"/></a>
  <a href="https://github.com/PayTechUz/payme-pkg/issues">
    <img src="https://img.shields.io/github/issues/PayTechUz/payme-pkg" />
  </a>
  <a href="https://pepy.tech/project/payme-pkg">
    <img src="https://static.pepy.tech/badge/payme-pkg" alt="PyPI - Downloads" />
  </a>
</p>

<p align="center">Welcome to payme-pkg, the open source payme SDK for Python.</p>

<p align="center">You can use it for test and production mode. Join our community and ask everything you need.</p>

<a href="https://docs.pay-tech.uz">
  <p align="center">Visit the full documentation for Merchant and Subscribe API</p>
</a>

<p align="center">
  <a href="https://youtu.be/7q7-c72tHpc?si=Sr0EAmEawWAFRk1m" target="_blank">
    <img src="https://img.shields.io/badge/Watch%20Demo-red?logo=youtube&logoColor=white&style=for-the-badge" 
         alt="Watch the YouTube Demo" 
         style="width: 150px; height: 30px; border-radius: 7px;" />
  </a>
</p>


## Installation

```shell
pip install payme-pkg
```

## Installation to Django

Add `'payme'` in to your settings.py

```python
INSTALLED_APPS = [
    ...
    'payme',
    ...
]
```

Add `'payme'` credentials inside to settings.py

One time payment (Однаразовый платеж) configuration settings.py

Example project: https://github.com/PayTechUz/shop-backend
```python
PAYME_ID = "your-payme-id"
PAYME_KEY = "your-payme-key"
PAYME_ACCOUNT_FIELD = "order_id"
PAYME_AMOUNT_FIELD = "total_amount"
PAYME_ACCOUNT_MODEL = "orders.models.Orders"
PAYME_ONE_TIME_PAYMENT = True
```

Multi payment (Накопительный) configuration settings.py

Example project: Coming soon
```python
PAYME_ID = "your-payme-id"
PAYME_KEY = "your-payme-key"
PAYME_ACCOUNT_FIELD = "id"
PAYME_ACCOUNT_MODEL = "clients.models.Client"
PAYME_ONE_TIME_PAYMENT = False
```

Create a new View that about handling call backs
```python
from payme.views import PaymeWebHookAPIView


class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")
```

Add a `payme` path to core of urlpatterns:

```python
from django.urls import path
from django.urls import include

from your_app.views import PaymeCallBackAPIView

urlpatterns = [
    ...
    path("payment/update/", PaymeCallBackAPIView.as_view()),
    ...
]
```

Run migrations
```shell
python manage.py migrate
```
🎉 Congratulations you have been integrated merchant api methods with django, keep reading docs. After successfull migrations check your admin panel and see results what happened.

## Generate Pay Link

Example to generate link:

- Input

```python
from payme import Payme

payme = Payme(payme_id="your-payme-id")
pay_link = payme.initializer.generate_pay_link(id=123456, amount=5000, return_url="https://example.com")
print(pay_link)
```

- Output

```
https://checkout.paycom.uz/bT15b3VyLXBheW1lLWlkO2FjLmlkPTEyMzQ1NjthPTUwMDAwMDtjPWh0dHBzOi8vZXhhbXBsZS5jb20=
```


## Generate Fallback Link


Example to generate fallback link:

- Input

The ID in the fallback is different from the merchant ID. You can get the ID from the Payme team.
```python
from payme import Payme

payme = Payme(payme_id="your-payme-id", fallback_id="your-fallback-id")

form_fields = {
    "driver_id": 12345,
    "amount": 1000
}

fallback_link = payme.initializer.generate_fallback_link(form_fields) # form field is optional
print(fallback_link)
```

- Output

```
https://payme.uz/fallback/merchant/?id=examplelinkgenerated&driver_id=12345&amount=1000
```
