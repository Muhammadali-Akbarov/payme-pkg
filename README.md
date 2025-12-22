<h1 align="center">Payme Software Development Kit</h1>

<p align="center">
  <a href="https://t.me/+lO97J78xBj45MzBi">
    <img src="https://img.shields.io/badge/Support%20Group-blue?logo=telegram&logoColor=white" alt="Support Group on Telegram"/>
  </a>
</p>

<p align="center">
  <a href="#table-of-contents"><img src="https://img.shields.io/static/v1?message=Documentation&logo=gitbook&logoColor=ffffff&label=%20&labelColor=5c5c5c&color=3F89A1"></a>
  <a href="https://t.me/+lO97J78xBj45MzBi"><img src="https://img.shields.io/badge/Support%2024/7-💬-FDA599?"/></a>
  <a href="https://github.com/PayTechUz/payme-pkg/issues">
    <img src="https://img.shields.io/github/issues/PayTechUz/payme-pkg" />
  </a>
  <a href="https://pepy.tech/project/payme-pkg">
    <img src="https://static.pepy.tech/badge/payme-pkg" alt="PyPI - Downloads" />
  </a>
</p>

<p align="center">Welcome to payme-pkg, the Payme SDK for Python.</p>

<p align="center">You can use it for test and production mode. Join our community and ask everything you need.</p>

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

## Table of Contents

- [Installation](#installation)
- [Django Integration](#django-integration)
- [Payme Client SDK](#payme-client-sdk)
  - [Initialization](#initialization)
  - [Cards API](#cards-api)
    - [Create Card](#create-card)
    - [Get Verify Code](#get-verify-code)
    - [Verify Card](#verify-card)
    - [Check Card](#check-card)
    - [Remove Card](#remove-card)
    - [Test Cards](#test-cards)
  - [Receipts API](#receipts-api)
    - [Create Receipt](#create-receipt)
    - [Pay Receipt](#pay-receipt)
    - [Send Receipt](#send-receipt)
    - [Cancel Receipt](#cancel-receipt)
    - [Check Receipt](#check-receipt)
    - [Get Receipt](#get-receipt)
    - [Get All Receipts](#get-all-receipts)
    - [Set Fiscal Data](#set-fiscal-data)
    - [Test Receipts](#test-receipts)
  - [Payment Initialization](#payment-initialization)
    - [Generate Pay Link](#generate-pay-link)
    - [Generate Fallback Link](#generate-fallback-link)

## Django Integration

Add `'payme'` in to your settings.py

```python
INSTALLED_APPS = [
    ...
    'payme',
    ...
]
```

Set your license API key as an environment variable (get your key at https://docs.pay-tech.uz/console or contact @muhammadali_me on Telegram):

```shell
export PAYTECH_LICENSE_API_KEY="your-license-api-key-here"
```

One time payment (Однаразовый платеж) configuration settings.py

Example project: https://github.com/PayTechUz/shop-backend
```python
PAYME_ID = "your-payme-id"
PAYME_KEY = "your-payme-key"
PAYME_ACCOUNT_FIELD = "order_id"
PAYME_AMOUNT_FIELD = "total_amount"
PAYME_ACCOUNT_MODEL = "orders.models.Orders"
PAYME_ONE_TIME_PAYMENT = True

PAYME_DISABLE_ADMIN = False # (optionally configuration if you want to disable change to True)

```

Create a new View that about handling call backs
```python
from payme.views import PaymeWebHookAPIView


class PaymeCallBackAPIView(PaymeWebHookAPIView):


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

## Payme Client SDK

The Payme SDK provides a unified client interface for working with all Payme services.

## Initialization

Initialize the Payme client with your credentials:

```python
from payme import Payme

# Basic initialization (for Cards API and Payment Links)
payme = Payme(
    payme_id="your-payme-id",
    is_test_mode=True,  # Optional: defaults to False
)

# Full initialization (for all features including Receipts API)
payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key",  # Required for Receipts API
    is_test_mode=True,
)
```

---

## Cards API

Manage card tokenization and verification.

### Create Card

Create a new card token.

```python
response = payme.cards_create(
    number="8600495473316478",
    expire="0399",  # MMYY format
    save=True,  # Optional: save card for future use
    timeout=10  # Optional: request timeout in seconds
)

print(response.result.card.token)  # Card token
print(response.result.card.number)  # Masked card number
```

### Get Verify Code

Request a verification code for a card.

```python
response = payme.cards_get_verify_code(
    token="card-token",
    timeout=10
)

print(response.result.sent)  # True if code was sent
print(response.result.phone)  # Phone number where code was sent
```

### Verify Card

Verify a card with the code received via SMS.

```python
response = payme.cards_verify(
    token="card-token",
    code="666666",  # Code from SMS
    timeout=10
)

print(response.result.card.verify)  # True if verified
```

### Check Card

Check the status of a card.

```python
response = payme.cards_check(
    token="card-token",
    timeout=10
)

print(response.result.card.verify)  # Verification status
```

### Remove Card

Remove a card token.

```python
response = payme.cards_remove(
    token="card-token",
    timeout=10
)

print(response.result.success)  # True if removed
```

### Test Cards

Run comprehensive tests for card operations.

```python
payme.cards_test()
```

---

## Receipts API

Manage payment receipts (requires `payme_key`).

### Create Receipt

Create a new payment receipt.

```python
response = payme.receipts_create(
    account={"order_id": 12345},
    amount=50000,  # Amount in tiyins (50000 tiyins = 500 UZS)
    description="Payment for order #12345",  # Optional
    detail={  # Optional
        "items": [
            {"name": "Product 1", "price": 25000, "quantity": 1},
            {"name": "Product 2", "price": 25000, "quantity": 1}
        ]
    },
    timeout=10
)

print(response.result.receipt._id)  # Receipt ID
```

### Pay Receipt

Pay a receipt using a card token.

```python
response = payme.receipts_pay(
    receipts_id="receipt-id",
    token="card-token",
    timeout=10
)

print(response.result.receipt.state)  # Payment state (4 = paid)
```

### Send Receipt

Send receipt details to a phone number.

```python
response = payme.receipts_send(
    receipts_id="receipt-id",
    phone="998901234567",
    timeout=10
)

print(response.result.success)  # True if sent
```

### Cancel Receipt

Cancel a receipt.

```python
response = payme.receipts_cancel(
    receipts_id="receipt-id",
    timeout=10
)

print(response.result.receipt.state)  # State (50 = cancelled)
```

### Check Receipt

Check the status of a receipt.

```python
response = payme.receipts_check(
    receipts_id="receipt-id",
    timeout=10
)

print(response.result.state)  # Current state
```

### Get Receipt

Get detailed information about a specific receipt.

```python
response = payme.receipts_get(
    receipts_id="receipt-id",
    timeout=10
)

print(response.result.receipt)  # Receipt details
```

### Get All Receipts

Get all receipts within a time range.

```python
response = payme.receipts_get_all(
    count=10,  # Number of receipts to retrieve
    from_=1609459200000,  # Start timestamp (milliseconds)
    to=1640995200000,  # End timestamp (milliseconds)
    offset=0,  # Pagination offset
    timeout=10
)

for receipt in response.result:
    print(receipt._id, receipt.amount)
```

### Set Fiscal Data

Set fiscal data for a receipt.

```python
response = payme.receipts_set_fiscal_data(
    receipt_id="receipt-id",
    qr_code_url="https://ofd.uz/check?t=123&s=456&r=789&c=2024",
    timeout=10
)

print(response.result.success)  # True if set
```

### Test Receipts

Run comprehensive tests for receipt operations.

```python
payme.receipts_test()
```

---

## Payment Initialization

Generate payment links for customers.

### Generate Pay Link

Generate a payment link for checkout.

```python
pay_link = payme.generate_pay_link(
    id=12345,  # Account ID
    amount=5000,  # Amount in UZS (will be converted to tiyins)
    return_url="https://example.com/success"
)

print(pay_link)
# Output: https://checkout.paycom.uz/bT1...
```

### Generate Fallback Link

Generate a fallback payment link with custom form fields.

```python
fallback_link = payme.generate_fallback_link(
    form_fields={  # Optional
        "driver_id": 12345,
        "amount": 1000
    }
)

print(fallback_link)
# Output: https://payme.uz/fallback/merchant/?id=...&driver_id=12345&amount=1000
```

**Note:** The fallback ID is different from the merchant ID. Contact the Payme team to get your fallback ID.
