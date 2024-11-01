<h1 align="center">Payme PKG</h1>


<p align="center">
  <a href="https://docs.pay-tech.uz"><img src="https://img.shields.io/static/v1?message=Documented%20on%20GitBook&logo=gitbook&logoColor=ffffff&label=%20&labelColor=5c5c5c&color=3F89A1"></a>
  <a href="https://github.com/PayTechUz/payme-pkg"><img src="https://img.shields.io/badge/Open_Source-❤️-FDA599?"/></a>
  <a href="t.me/+DK7n7lKx8GY5ZDZi"><img src="https://img.shields.io/badge/Community-Join%20Us-blueviolet"/></a>
  <a href="https://github.com/PayTechUz/payme-pkg/issues"><img src="https://img.shields.io/github/issues/gitbookIO/gitbook"/></a>
</p>

<p align="center">Welcome to payme-pkg, the open source payme sdk for python.</p>

<p align="center">You can use for test and production mode. Join our community and ask everything you need.
</p>
<a href="https://docs.pay-tech.uz">
<p align="center">Visit to full documentation for Merchant and Subcribe Api</p>
</a>
<p align="center">
 <img style="width: 60%;" src="https://i.postimg.cc/WbD32bHC/payme-pkg-demo-m4a.gif">
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

One time payment configuration settings.py
```python
PAYME_ID = "your-payme-id"
PAYME_KEY = "your-payme-key"
PAYME_ACCOUNT_FIELD = "id"
PAYME_AMOUNT_FIELD = "total_amount"
PAYME_ACCOUNT_MODEL = "orders.models.Orders"
PAYME_ONE_TIME_PAYMENT = True
```

Multi payment configuration settings.py
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
python3 manage.py makemigrations && python manage.py migrate
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
