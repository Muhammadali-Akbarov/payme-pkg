# Payme Uzbekistan Integration Uzcard and Humo
<p align="center">
<a href="https://youtu.be/r2RO3kJVP7g">
<img style="width: 60%;" src="https://i.postimg.cc/WbD32bHC/payme-pkg-demo-m4a.gif">
</a>
</p>
Support Group - <a href="https://t.me/+Ng1axYLNyBAyYTRi">Telegram</a> <br/>
YouTube - <a href="https://youtu.be/sJORIyykHcw">Watch Video</a><br/>
Implementation Sample - https://github.com/PayTechUz/payme-sample

## Installation

```shell
pip install payme-pkg
```

### Test-Credentials

```
Card Numer: 8600 4954 7331 6478 Expire Date: 03/99 SMS Code: 666666
Card Numer: 8600 0691 9540 6311 Expire Date: 03/99 SMS Code: 666666
```

## Documentation

- [Merchant API](#merchant-api)
- [Generate Pay Link](#generate-pay-link)

- Subscribe Cards

  - [Cards Create](#cards-create)
  - [Cards Get Verify Code](#cards-get-verify-code)
  - [Cards Verify](#cards-verify)
  - [Cards Check](#cards-check)
  - [Cards Remove](#cards-remove)

- Subscribe Receipts
  - [Receipts Create](#receipts-create)
  - [Receipts Pay](#receipts-pay)
  - [Receipts Send](#receipts-send)
  - [Receipts Cancel](#receipts-cancel)
  - [Receipts Check](#receipts-check)
  - [Receipts Get](#receipts-get)
  - [Receipts Get All ](#receipts-get-all)

# Merchant API

## Installation to Django

Add `'payme'` in to your settings.

```python
INSTALLED_APPS = [
    ...
    'payme',
    ...
]
```

Add `'payme'` credentials inside to settings.

One time payment configuration
```python
PAYME_ID = "670cb597e51de1c6a3a5934b"
PAYME_KEY = "KCR4W1kzqPxxUeW&BHNM0AOtR3?&0@E%R?P@"
PAYME_ACCOUNT_FIELD = "id"
PAYME_AMOUNT_FIELD = "total_amount"
PAYME_ACCOUNT_MODEL = "orders.models.Orders"
PAYME_ONE_TIME_PAYMENT = True
```

Multi payment configuration
```python
PAYME_ID = "670cb597e51de1c6a3a5934b"
PAYME_KEY = "KCR4W1kzqPxxUeW&BHNM0AOtR3?&0@E%R?P@"
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
    path("payments/updates/", PaymeCallBackAPIView.as_view()),
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

## Cards Create

Example for cards create method for to generate token from card:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.cards.create(
    number="8600495473316478",
    expire="0399",
    save=True
)
print("response:", response)
print("token:", response.result.card.token)
```

- Response

```python
response: CardsCreateResponse(jsonrpc='2.0', result=Result(card=Card(number='860049******6478', expire='03/99', token='6723b098ce33ffc53780c5cf_dQG8dcyUXKA4cBrUO9wPoqaZBM34HzfwO9EONqkUZAUMK3OS23vaRQuvK7J6a2uGCTERZxhR8NzT82r3MDDSncdgeDQ2gioxANuU357Pw9Kp1tqhiCmJ3SjMzi2QzpxYcQdnbf5AhSsyQI4C2kaIasYp4vCRmZm8v1TxneJjKf2PB6Ra6gnPW59XRrdy6qDDhtVFB1umGtrEJEaR731JhVbk8eViwHEPWEKYwaQSjNqTZYWmutGV34kJHyXTf3eJGW1A5TQphRDUBBEbFSGWPHOIcQbO3WSJirQ8hWobv6Qx2EbxfsJ2WQnF0qsuEKF7HoerEfAKHroJyEW2hTvHHkMNtUU8NNQEaQA5iB7JiQsOb16F5HNXpTXE8VuDbUYK2YGtxi', recurrent=True, verify=False, type='22618', number_hash='cb7ea1f6238ce309314b1a1f722faca454d3b85b')))

token: 6723b098ce33ffc53780c5cf_dQG8dcyUXKA4cBrUO9wPoqaZBM34HzfwO9EONqkUZAUMK3OS23vaRQuvK7J6a2uGCTERZxhR8NzT82r3MDDSncdgeDQ2gioxANuU357Pw9Kp1tqhiCmJ3SjMzi2QzpxYcQdnbf5AhSsyQI4C2kaIasYp4vCRmZm8v1TxneJjKf2PB6Ra6gnPW59XRrdy6qDDhtVFB1umGtrEJEaR731JhVbk8eViwHEPWEKYwaQSjNqTZYWmutGV34kJHyXTf3eJGW1A5TQphRDUBBEbFSGWPHOIcQbO3WSJirQ8hWobv6Qx2EbxfsJ2WQnF0qsuEKF7HoerEfAKHroJyEW2hTvHHkMNtUU8NNQEaQA5iB7JiQsOb16F5HNXpTXE8VuDbUYK2YGtxi
```

## Cards Get Verify Code

Example for cards get verify:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.cards.get_verify_code(
    token="card-token"
)
print("response", response)
print("response is_sent", response.result.sent)
```

- Response

```python
response GetVerifyResponse(jsonrpc='2.0', result=VerifyResult(sent=True, phone='99811*****36', wait=60000))
response is_sent True
```

## Cards Verify

Example for cards verify method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)

response = payme.cards.verify(
    token="card-token",
    code="666666"
)
print("response", response)
print("response verify", response.result.card.verify)
```

- Response

```python
response VerifyResponse(jsonrpc='2.0', result=Result(card=Card(number='860049******6478', expire='03/99', token='6723b22dce33ffc53780c5d0_H1VcV5w8HVXeEmX2NQeK0WeWN3noUUtzysNtPD3mPYB0vxGK7xP1aok1s2DhPGD21qgSGwUpseYfuNeGoUehsXPnTTx1Eacis2jNCdfYPcsmqWB60XqwiYuwSy6EdVQxzEv6Pu8mdR06S1NQSKWBc6hgzgPGSpDkUrbTEKhyWo0QgK0hSTP9bxPt5KHCwuvJUDVHkAfgI0P4ACtgTJhvRoP6ypAC7Y3NvGOU2CrgfikdKym8Ev8hjbwo3hdPfdeGCHu3ZOEbAWWVeTQMDHACPYRnDPcgh8fOehK6j21ZgqRa7oUAxStgkUhJSbT5bXH74p5OBsZgWYW1pgPnvUGjH9uNs4noXqxaytE4sRNkh9OQfuKzgbKhmYSw0gIszeWTq16srj', recurrent=True, verify=True, type='22618', number_hash='cb7ea1f6238ce309314b1a1f722faca454d3b85b')))

response verify True
```

## Cards Check

Example for cards check:

- Request

```python
response = payme.cards.check(token="card-token")
print("response", response)
```

- Response

```python
response CheckResponse(jsonrpc='2.0', result=Result(card=Card(number='860049******6478', expire='03/99', token='6723b22dce33ffc53780c5d0_H1VcV5w8HVXeEmX2NQeK0WeWN3noUUtzysNtPD3mPYB0vxGK7xP1aok1s2DhPGD21qgSGwUpseYfuNeGoUehsXPnTTx1Eacis2jNCdfYPcsmqWB60XqwiYuwSy6EdVQxzEv6Pu8mdR06S1NQSKWBc6hgzgPGSpDkUrbTEKhyWo0QgK0hSTP9bxPt5KHCwuvJUDVHkAfgI0P4ACtgTJhvRoP6ypAC7Y3NvGOU2CrgfikdKym8Ev8hjbwo3hdPfdeGCHu3ZOEbAWWVeTQMDHACPYRnDPcgh8fOehK6j21ZgqRa7oUAxStgkUhJSbT5bXH74p5OBsZgWYW1pgPnvUGjH9uNs4noXqxaytE4sRNkh9OQfuKzgbKhmYSw0gIszeWTq16srj', recurrent=True, verify=True, type='22618', number_hash='cb7ea1f6238ce309314b1a1f722faca454d3b85b')))
```

## Cards Remove

Example for cards create method for to generate token from card:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.cards.remove(
    token="card-token",
)
print("response", response)
print("response result success", response.result.success)
```

- Response

```python
response RemoveResponse(jsonrpc='2.0', result=RemoveCardResult(success=True))
response result success True
```

## Receipts Create

Example for receipts create method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
account = {
    "id": 123456
}
response = payme.receipts.create(
    account=account,
    amount=700000,
    description="Test payment for order-id: 123456",
    detail={
        "order_id": 123456,
        "customer_name": "John Doe"
    }
)
print("response", response)
print("response receipt_id", response.result.receipt._id)
```

- Response

```python
response CreateResponse(result=CreateResult(receipt=Receipt(_id='6723b6a8b64ab20e492e81ed', create_time=1730393768622, pay_time=0, cancel_time=0, state=0, type=2, external=False, operation=-1, category=None, error=None, description='Test payment for order-id: 123456', detail=Detail(discount=None, shipping=None, items=None), currency=860, commission=0, card=None, creator=None, payer=None, amount=700000, account=[{'name': 'transaction', 'title': 'Номер чека', 'value': '31096', 'main': True}, {'name': 'commission', 'title': 'Стоимость услуги', 'value': '0.00 сум'}], merchant={'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': 'Internet', 'terms': None}, processing_id=None, meta=Meta(source='subscribe', owner='5feb5dd783c40aed047fe655', host='app-test-172-17-25-21'))))

response receipt_id 6723b6a8b64ab20e492e81ed
```

## Receipts Pay

Example for receipts pay method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.receipts.pay(
    receipts_id="6723b85fb64ab20e492e8250",
    token="card-token"
)
print("response", response)
print("response state", response.result.receipt.state)
```

- Response

```python
PayResponse(result=CreateResult(receipt=Receipt(_id='6723b85fb64ab20e492e8250', create_time=1730394213942, pay_time=1730394214080, cancel_time=0, state=4, type=2, external=False, operation=-1, category=None, error=None, description='DESC', detail=Detail(discount=None, shipping=None, items=None), currency=860, commission=0, card={'number': '860049******6478', 'expire': '9903'}, creator=None, payer=Payer(phone='998116363636'), amount=100, account=[{'name': 'transaction', 'title': 'Номер чека', 'value': '31097', 'main': True}, {'name': 'commission', 'title': 'Стоимость услуги', 'value': '0.00 сум'}], merchant={'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': 'Internet', 'terms': None}, processing_id=0, meta=Meta(source='subscribe', owner='5feb5dd783c40aed047fe655', host='app-test-172-17-25-21'))))

response state 4
```

## Receipts Send

Example for receipts send method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)

response = payme.receipts.send(
    receipts_id="6723b91fb64ab20e492e827b",
    phone="998901304527"
)

print("response", response)
print("response success", response.result.success)
```

- Response

```python
response SendResponse(result=SendResult(success=True))
response success True
```

## Receipts Cancel

Example for receipts cancel method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.receipts.cancel(
    receipts_id="6723b91fb64ab20e492e827b",
)

print("response", response)
print("response state", response.result.receipt.state)
```

- Response

```python
response CancelResponse(result=CreateResult(receipt=Receipt(_id='6723b91fb64ab20e492e827b', create_time=1730394399716, pay_time=0, cancel_time=1730394529899, state=50, type=2, external=False, operation=-1, category=None, error=None, description='DESC', detail=Detail(discount=None, shipping=None, items=None), currency=860, commission=0, card=None, creator=None, payer=None, amount=100, account=[{'name': 'transaction', 'title': 'Номер чека', 'value': '31098', 'main': True}], merchant={'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': 'Internet', 'terms': None}, processing_id=None, meta=Meta(source='subscribe', owner='5feb5dd783c40aed047fe655', host='app-test-172-17-25-21'))))

response state 50
```

## Receipts Check

Example for receipts check method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.receipts.check(
    receipts_id="6723b91fb64ab20e492e827b",
)

print("response", response)
print("response state", response.result.receipt.state)
```

- Response
```python
response CheckResponse(result=CheckResult(state=50))
response state 50
```

## Receipts Get

Example for receipts get method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.receipts.get(
    receipts_id="6723b91fb64ab20e492e827b",
)

print("response", response)
```

- Response

```python
response GetResponse(result=CreateResult(receipt=Receipt(_id='6723b91fb64ab20e492e827b', create_time=1730394399716, pay_time=0, cancel_time=1730394529899, state=50, type=2, external=False, operation=-1, category=None, error=None, description='DESC', detail=Detail(discount=None, shipping=None, items=None), currency=860, commission=0, card=None, creator=None, payer=None, amount=100, account=[{'name': 'transaction', 'title': 'Номер чека', 'value': '31098', 'main': True}, {'name': 'commission', 'title': 'Стоимость услуги', 'value': '0.00 сум'}], merchant={'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': 'Internet', 'terms': None}, processing_id=None, meta=Meta(source='subscribe', owner='5feb5dd783c40aed047fe655', host='app-test-172-17-25-21'))))
```

## Receipts Get All

Example for receipts get all method:

- Request

```python
from payme import Payme

payme = Payme(
    payme_id="your-payme-id",
    payme_key="your-payme-key", # test key use prod key for production mode
    is_test_mode=True # use is_test_mode=False for production mode
)
response = payme.receipts.get_all(
    count=5,
    from_=1730322122000,
    to=1730398982000,
    offset=10
)
for receipt in response.result:
    print(receipt)

```

- Response

```python
{'_id': '67239f59b64ab20e492e7cd7', 'create_time': 1730387802076, 'cashback_receipt': None, 'pay_time': 1730387802258, 'cancel_time': 0, 'state': 4, 'type': 2, 'external': False, 'operation': -1, 'category': None, 'error': None, 'description': 'Test receipt', 'detail': {'discount': None, 'shipping': None, 'items': None}, 'amount': 1000, 'currency': 860, 'commission': 0, 'account': [{'name': 'transaction', 'title': {'ru': 'Номер чека', 'uz': 'Chek raqami'}, 'value': 31088, 'main': True}, {'name': 'commission', 'title': {'ru': 'Стоимость услуги', 'en': 'Service Cost', 'uz': 'Xizmat narxi'}, 'value': '0.00', 'currency': {'en': 'sum', 'ru': 'сум', 'uz': 'so’m', 'uz_cyrl_uz': 'сўм'}}], 'card': {'number': '8600495473316478', 'expire': '9903'}, 'creator': None, 'payer': {'phone': '998116363636'}, 'merchant': {'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': {'ru': 'Internet', 'uz': 'Internet'}, 'terms': None}, 'meta': {'source': 'subscribe', 'owner': '5feb5dd783c40aed047fe655', 'host': 'app-test-172-17-25-21'}, 'processing_id': 0}
{'_id': '67239cceb64ab20e492e7c3e', 'create_time': 1730387150024, 'pay_time': 0, 'cancel_time': 1730387150116, 'state': 50, 'type': 2, 'external': False, 'operation': -1, 'category': None, 'error': None, 'description': 'Test receipt', 'detail': {'discount': None, 'shipping': None, 'items': None}, 'amount': 1000, 'currency': 860, 'commission': 0, 'account': [{'name': 'transaction', 'title': {'ru': 'Номер чека', 'uz': 'Chek raqami'}, 'value': 31087, 'main': True}, {'name': 'commission', 'title': {'ru': 'Стоимость услуги', 'en': 'Service Cost', 'uz': 'Xizmat narxi'}, 'value': '0.00', 'currency': {'en': 'sum', 'ru': 'сум', 'uz': 'so’m', 'uz_cyrl_uz': 'сўм'}}], 'card': None, 'creator': None, 'payer': None, 'merchant': {'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': {'ru': 'Internet', 'uz': 'Internet'}, 'terms': None}, 'meta': {'source': 'subscribe', 'owner': '5feb5dd783c40aed047fe655', 'host': 'app-test-172-17-25-21', 'source_cancel': 'subscribe'}, 'processing_id': None}
{'_id': '67239ccdb64ab20e492e7c3d', 'create_time': 1730387149794, 'pay_time': 0, 'cancel_time': 0, 'state': 0, 'type': 2, 'external': False, 'operation': -1, 'category': None, 'error': None, 'description': 'Test receipt', 'detail': {'discount': None, 'shipping': None, 'items': None}, 'amount': 1000, 'currency': 860, 'commission': 0, 'account': [{'name': 'transaction', 'title': {'ru': 'Номер чека', 'uz': 'Chek raqami'}, 'value': 31086, 'main': True}, {'name': 'commission', 'title': {'ru': 'Стоимость услуги', 'en': 'Service Cost', 'uz': 'Xizmat narxi'}, 'value': '0.00', 'currency': {'en': 'sum', 'ru': 'сум', 'uz': 'so’m', 'uz_cyrl_uz': 'сўм'}}], 'card': None, 'creator': None, 'payer': None, 'merchant': {'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': {'ru': 'Internet', 'uz': 'Internet'}, 'terms': None}, 'meta': {'source': 'subscribe', 'owner': '5feb5dd783c40aed047fe655', 'host': 'app-test-172-17-25-21'}, 'processing_id': None}
{'_id': '67239ccdb64ab20e492e7c3c', 'create_time': 1730387149585, 'cashback_receipt': None, 'pay_time': 1730387149688, 'cancel_time': 0, 'state': 4, 'type': 2, 'external': False, 'operation': -1, 'category': None, 'error': None, 'description': 'Test receipt', 'detail': {'discount': None, 'shipping': None, 'items': None}, 'amount': 1000, 'currency': 860, 'commission': 0, 'account': [{'name': 'transaction', 'title': {'ru': 'Номер чека', 'uz': 'Chek raqami'}, 'value': 31085, 'main': True}, {'name': 'commission', 'title': {'ru': 'Стоимость услуги', 'en': 'Service Cost', 'uz': 'Xizmat narxi'}, 'value': '0.00', 'currency': {'en': 'sum', 'ru': 'сум', 'uz': 'so’m', 'uz_cyrl_uz': 'сўм'}}], 'card': {'number': '8600495473316478', 'expire': '9903'}, 'creator': None, 'payer': {'phone': '998116363636'}, 'merchant': {'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': {'ru': 'Internet', 'uz': 'Internet'}, 'terms': None}, 'meta': {'source': 'subscribe', 'owner': '5feb5dd783c40aed047fe655', 'host': 'app-test-172-17-25-21'}, 'processing_id': 0}
{'_id': '67239beeb64ab20e492e7c0c', 'create_time': 1730386926766, 'pay_time': 0, 'cancel_time': 1730386926859, 'state': 50, 'type': 2, 'external': False, 'operation': -1, 'category': None, 'error': None, 'description': 'Test receipt', 'detail': {'discount': None, 'shipping': None, 'items': None}, 'amount': 1000, 'currency': 860, 'commission': 0, 'account': [{'name': 'transaction', 'title': {'ru': 'Номер чека', 'uz': 'Chek raqami'}, 'value': 31084, 'main': True}, {'name': 'commission', 'title': {'ru': 'Стоимость услуги', 'en': 'Service Cost', 'uz': 'Xizmat narxi'}, 'value': '0.00', 'currency': {'en': 'sum', 'ru': 'сум', 'uz': 'so’m', 'uz_cyrl_uz': 'сўм'}}], 'card': None, 'creator': None, 'payer': None, 'merchant': {'_id': '5feb5dd783c40aed047fe655', 'name': 'OO Mytaxi Test', 'organization': 'ЧП «Саидахмад Абдурахманов»', 'address': '', 'business_id': '5b0fd34b8f79903b6a38613e', 'epos': {'merchantId': '106600000050000', 'terminalId': '20660000'}, 'restrictions': None, 'date': 1609260503764, 'logo': None, 'type': {'ru': 'Internet', 'uz': 'Internet'}, 'terms': None}, 'meta': {'source': 'subscribe', 'owner': '5feb5dd783c40aed047fe655', 'host': 'app-test-172-17-25-21', 'source_cancel': 'subscribe'}, 'processing_id': None}
```
