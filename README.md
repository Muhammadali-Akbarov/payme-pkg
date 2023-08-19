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

```python
PAYME: dict = {
    'PAYME_ID': 'payme-id',
    'PAYME_KEY': 'payme-key',
    'PAYME_URL': 'payme-checkout-url',
    'PAYME_CALL_BACK_URL': 'your-callback-url', # merchant api callback url
    'PAYME_MIN_AMOUNT': 'payme-min-amount', # integer field
    'PAYME_ACCOUNT': 'order-id',
}

ORDER_MODEL = 'your_app.models.Your_Order_Model'
```

Create a new View that about handling call backs
```python
from payme.views import MerchantAPIView


class PaymeCallBackAPIView(MerchantAPIView):
    def create_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"create_transaction for order_id: {order_id}, response: {action}")

    def perform_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"perform_transaction for order_id: {order_id}, response: {action}")

    def cancel_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"cancel_transaction for order_id: {order_id}, response: {action}")
```

Add a `payme` path to core of urlpatterns:

```python
from django.urls import path
from django.urls import include

from your_app.views import PaymeCallBackAPIView

urlpatterns = [
    ...
    path("payments/merchant/", PaymeCallBackAPIView.as_view()),
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
from pprint import pprint

from payme.methods.generate_link import GeneratePayLink

pay_link = GeneratePayLink(
  order_id=999,
  amount=9999
).generate_link()

pprint(pay_link)
```

- Output

```
Link: https://checkout.paycom.uz/bT01ZTczMGU4ZTBiODUyYTQxN2FhNDljZWI7YWMub3JkZXItaWQ9OTk5O2E9OTk5OTtjPXlvdXItY2FsbGJhY2stdXJs
```

## Cards Create

Example for cards create method for to generate token from card:

- Request

```python
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards

client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id
)

resp = client.cards_create(
    number="8600069195406311",
    expire="0399",
    save=True
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "card": {
      "number": "860006******6311",
      "expire": "03/99",
      "token": "63119784d15d8d8d093b37b8_ADHrAykwnAIc2hm4hPPriktZ8nnuvR96S9Kzmjb3Fcix25IrJmMKrGxP9VUEP9rRDKRhtYjUw0vsXON7PYEyMCHtDKpMuM4krrIk8jdnyK7bXkSBSCyiGs2aahIrep6TSodIAxqutMJ4g3O8FZ8vC1DSMKzOaX0UF8fDKNexXV039Qnj4bNQc6NcpKGJn0wUX8d0RBqkmKid4WyUQnT987ZQDM2mT2IGNZtugvN4tDJTXBVTpqCWkXnZ0YWj64Ye0ztr91Mibtndo0Y1s5nCA6wufUZZugJ6c7rse19XNFSSieFM7AWi9VqybMe4eeWiZEBriAbFhrf8kQvrpBmwUEp05GjvFMgH0ku3vyUtSuJI36exHheXuJK66KstcX1i69EaF3",
      "recurrent": true,
      "verify": false,
      "type": "22618"
    }
  }
}
```

## Cards Get Verify Code

Example for cards get verify:

- Request

```python
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id
)

resp = client.card_get_verify_code(
    token="630e5ffdd15d8d8d093b379b_2fsaoABWafecn20kofV4PFafFZjeGDWS9adM1PmboQaEZbbaxMcnaskctMbU9Iv8qgrOuKGz8SnjvZvYXDK64m1eS9gA5jZ7BBRaQybMXrDPtFPJ1fwek5B1KoIv5cMiCWYXj7ezpYEdJAKTIQw0Np9HsTXjqco4gQG3m8MOfeH9ovkdm66O6yj45oKXRmJyAK5i0SchXNNomACH3Oq80KyoRE1VoBRxvoKyMkOx0xcepXovxK9d3v26a8z7UtyokwY33N8MupviM3A5WHB5Xh35WZJJyFnxTSi1vvnYnG7uVd6Bb1GjV2yAHnimss8aEZGW5V7ZiPrhf8r6WJAeHciYDGK3msRKZJBQTfjgOdE9tGrEnMezVkxr1JXX0xSn5qqec2"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "sent": true,
    "phone": "99890*****66",
    "wait": 60000
  }
}
```

## Cards Verify

Example for cards verify method:

- Request

```python
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id
)

resp = client.cards_verify(
    verify_code="666666",
    token="630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "card": {
      "number": "860006******6311",
      "expire": "03/99",
      "token": "63118a5dd15d8d8d093b37b7_X2j34OIJPnROfsgzYZCZ0w7OcC50zzwiowTsotEVO1uUbxkzaDrvdOno6jicQTrcRmxvibxrye4vUS3AynTNPaPCTGpfk3RCKmT9NaOAyyTmctAjWsjwvqGR5XUzAP1Xcx12GkhuQi6VJ4BeaIXOokSRu06rRjaivmJQ8HTiJiR9b3OmZtrhkIRNcNXnnp9zYm1mFP4BuqGpS8BMnY0ASIE6ffxWykjgBcDTAfWBFt4mg7O9Dsvx0aj3IB8z3RIbZYtDZJnUVhCZrwW7ONVI9uEAdxNthorjO6PbV7TQ8XCjrztgGf6uCtOwwxasiIUVZN6tCVDk8A8NvVSUzUHXQHVkaPn5heJNa3K4WsffIckq7SwMbiw3UbawipeZKyD3iwk1Km",
      "recurrent": true,
      "verify": true,
      "type": "22618"
    }
  }
}
```

## Cards Check

Example for cards check:

- Request

```python
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id
)

resp = client.cards_check(
    token="630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "card": {
      "number": "860006******6311",
      "expire": "03/99",
      "token": "63119b36d15d8d8d093b37c1_IJtHxZ46h5viyo8RIJCmQyE8qBw6PUWUdFKTMCVWrPoMMi4kJYsKyVdjQrIx6a12jDfEPVhhEqWm94FYvYh7IEjIs4xn0n3mM8Quw5dhd6ZT0dOK6u1spqWRMIDBpDMhHj2Ga8zZMAfeoiDAcrWScXS1AP2tkQHcJ40rBzHGHS6DoVeIheF70c0wO1kVQG0G5hDWguSGf2ZRFcBtpabv5BQkqSchxWKdCSVPIGiS6X7eF8YStdz1aGPzFyjDbaKT0vXNUMbQ7gaKh4PeQbruVVwFDfeIWqGeNmgCCPU4X0wCHFjTt8K61e9VOauNeU81ckoKHD8XGzCwGFJHrC4sHvNv4no3RifWhHCQF9GmFKf8cP2qh4pqTKwu3gOITaX5Ss71tC",
      "recurrent": true,
      "verify": true,
      "type": "22618"
    }
  }
}
```

## Cards Remove

Example for cards create method for to generate token from card:

- Request

```python
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id
)

resp = client.cards_remove(
    token="630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true
  }
}
```

## Receipts Create

Example for receipts create method:

- Request

```python
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id,
    paycom_key=$paycom_key
)

resp = rclient.receipts_create(
    amount=10000,
    order_id="1"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "receipt": {
      "_id": "63119becc4420cbf2712a24c",
      "create_time": 1662098412270,
      "pay_time": 0,
      "cancel_time": 0,
      "state": 0,
      "type": 2,
      "external": false,
      "operation": -1,
      "category": null,
      "error": null,
      "description": "",
      "detail": null,
      "amount": 400000,
      "currency": 860,
      "commission": 0,
      "account": [
        {
          "name": "transaction",
          "title": "Номер чека",
          "value": "2326",
          "main": true
        }
      ],
      "card": null,
      "merchant": {
        "_id": "5e730e8e0b852a417aa49ceb",
        "name": "test",
        "organization": "ЧП «test test»",
        "address": "",
        "business_id": "5e730e740b852a417aa49cea",
        "epos": {
          "merchantId": "106600000050000",
          "terminalId": "20660000"
        },
        "date": 1584598670296,
        "logo": null,
        "type": "Internet",
        "terms": null
      },
      "meta": {
        "source": "subscribe",
        "owner": "5e730e8e0b852a417aa49ceb"
      },
      "processing_id": null
    }
  }
}
```

## Receipts Pay

Example for receipts pay method:

- Request

```python
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id,
    paycom_key=$paycom_key
)

resp = rclient.receipts_pay(
    invoice_id="631186b6c4420cbf2712a243",
    token="63118a5dd15d8d8d093b37b7_X2j34OIJPnROfsgzYZCZ0w7OcC50zzwiowTsotEVO1uUbxkzaDrvdOno6jicQTrcRmxvibxrye4vUS3AynTNPaPCTGpfk3RCKmT9NaOAyyTmctAjWsjwvqGR5XUzAP1Xcx12GkhuQi6VJ4BeaIXOokSRu06rRjaivmJQ8HTiJiR9b3OmZtrhkIRNcNXnnp9zYm1mFP4BuqGpS8BMnY0ASIE6ffxWykjgBcDTAfWBFt4mg7O9Dsvx0aj3IB8z3RIbZYtDZJnUVhCZrwW7ONVI9uEAdxNthorjO6PbV7TQ8XCjrztgGf6uCtOwwxasiIUVZN6tCVDk8A8NvVSUzUHXQHVkaPn5heJNa3K4WsffIckq7SwMbiw3UbawipeZKyD3iwk1Km",
    phone="998901304527"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": {
    "receipt": {
      "_id": "63119becc4420cbf2712a24c",
      "create_time": 1662098438706,
      "pay_time": 1662098438804,
      "cancel_time": 0,
      "state": 4,
      "type": 2,
      "external": false,
      "operation": -1,
      "category": null,
      "error": null,
      "description": "",
      "detail": null,
      "amount": 400000,
      "currency": 860,
      "commission": 0,
      "account": [
        {
          "name": "transaction",
          "title": "Номер чека",
          "value": "2326",
          "main": true
        }
      ],
      "card": {
        "number": "860006******6311",
        "expire": "9903"
      },
      "merchant": {
        "_id": "5e730e8e0b852a417aa49ceb",
        "name": "test",
        "organization": "ЧП «test test»",
        "address": "",
        "business_id": "5e730e740b852a417aa49cea",
        "epos": {
          "merchantId": "106600000050000",
          "terminalId": "20660000"
        },
        "date": 1584598670296,
        "logo": null,
        "type": "Internet",
        "terms": null
      },
      "meta": {
        "source": "subscribe",
        "owner": "5e730e8e0b852a417aa49ceb"
      },
      "processing_id": 0
    }
  }
}
```

## Receipts Send

Example for receipts send method:

- Request

```python
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id,
    paycom_key=$paycom_key
)

resp = rclient.receipts_send(
    invoice_id="631186b6c4420cbf2712a243",
    phone="998901304527"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": {
    "success": true
  }
}
```

## Receipts Cancel

Example for receipts cancel method:

- Request

```python
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id,
    paycom_key=$paycom_key
)

resp = rclient.receipts_cancel(
    invoice_id="63119303c4420cbf2712a245"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": {
    "receipt": {
      "_id": "63119becc4420cbf2712a24c",
      "create_time": 1662098438706,
      "pay_time": 1662098438804,
      "cancel_time": 0,
      "state": 21,
      "type": 2,
      "external": false,
      "operation": -1,
      "category": null,
      "error": null,
      "description": "",
      "detail": null,
      "amount": 400000,
      "currency": 860,
      "commission": 0,
      "account": [
        {
          "name": "transaction",
          "title": "Номер чека",
          "value": "2326",
          "main": true
        }
      ],
      "card": {
        "number": "860006******6311",
        "expire": "9903"
      },
      "merchant": {
        "_id": "5e730e8e0b852a417aa49ceb",
        "name": "test",
        "organization": "ЧП «test test»",
        "address": "",
        "business_id": "5e730e740b852a417aa49cea",
        "epos": {
          "merchantId": "106600000050000",
          "terminalId": "20660000"
        },
        "date": 1584598670296,
        "logo": null,
        "type": "Internet",
        "terms": null
      },
      "meta": {
        "source": "subscribe",
        "owner": "5e730e8e0b852a417aa49ceb",
        "source_cancel": "subscribe"
      },
      "processing_id": null
    }
  }
}
```

## Receipts Check

Example for receipts check method:

- Request

```python
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id,
    paycom_key=$paycom_key
)

resp = rclient.receipts_check(
    invoice_id="63119303c4420cbf2712a245"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": {
    "state": 0
  }
}
```

## Receipts Get

Example for receipts get method:

- Request

```python
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id,
    paycom_key=$paycom_key
)

resp = rclient.reciepts_get(
    invoice_id="6311946bc4420cbf2712a247"
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": {
    "receipt": {
      "_id": "6311946bc4420cbf2712a247",
      "create_time": 1662096491076,
      "pay_time": 0,
      "cancel_time": 0,
      "state": 0,
      "type": 2,
      "external": false,
      "operation": -1,
      "category": null,
      "error": null,
      "description": "",
      "detail": null,
      "amount": 400000,
      "currency": 860,
      "commission": 0,
      "account": [
        {
          "name": "transaction",
          "title": "Номер чека",
          "value": "2325",
          "main": true
        }
      ],
      "card": null,
      "merchant": {
        "_id": "5e730e8e0b852a417aa49ceb",
        "name": "test",
        "organization": "ЧП «test test»",
        "address": "",
        "business_id": "5e730e740b852a417aa49cea",
        "epos": {
          "merchantId": "106600000050000",
          "terminalId": "20660000"
        },
        "date": 1584598670296,
        "logo": null,
        "type": "Internet",
        "terms": null
      },
      "meta": {
        "source": "subscribe",
        "owner": "5e730e8e0b852a417aa49ceb"
      },
      "processing_id": null
    }
  }
}
```

## Receipts Get All

Example for receipts get all method:

- Request

```python
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id=$paycom_id,
    paycom_key=$paycom_key
)

resp = rclient.reciepts_get_all(
    count=2,
    _from=1636398000000,
    to=1636398000000,
    offset=0
)

pprint(resp)
```

- Response

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": [
    {
      "_id": "6311946bc4420cbf2712a247",
      "create_time": 1662096491076,
      "pay_time": 0,
      "cancel_time": 0,
      "state": 0,
      "type": 2,
      "external": false,
      "operation": -1,
      "category": null,
      "error": null,
      "description": "",
      "detail": null,
      "amount": 400000,
      "currency": 860,
      "commission": 0,
      "account": [
        {
          "name": "transaction",
          "title": {
            "ru": "Номер чека",
            "uz": "Chek raqami"
          },
          "value": 2325,
          "main": true
        }
      ],
      "card": null,
      "merchant": {
        "_id": "5e730e8e0b852a417aa49ceb",
        "name": "test",
        "organization": "ЧП «test test»",
        "address": "",
        "business_id": "5e730e740b852a417aa49cea",
        "epos": {
          "merchantId": "106600000050000",
          "terminalId": "20660000"
        },
        "date": 1584598670296,
        "logo": null,
        "type": {
          "ru": "Internet",
          "uz": "Internet"
        },
        "terms": null
      },
      "meta": {
        "source": "subscribe",
        "owner": "5e730e8e0b852a417aa49ceb"
      },
      "processing_id": null
    },
    {
      "_id": "63119303c4420cbf2712a245",
      "create_time": 1662096131667,
      "pay_time": 0,
      "cancel_time": 1662096182979,
      "state": 50,
      "type": 2,
      "external": false,
      "operation": -1,
      "category": null,
      "error": null,
      "description": "",
      "detail": null,
      "amount": 400000,
      "currency": 860,
      "commission": 0,
      "account": [
        {
          "name": "transaction",
          "title": {
            "ru": "Номер чека",
            "uz": "Chek raqami"
          },
          "value": 2324,
          "main": true
        }
      ],
      "card": null,
      "merchant": {
        "_id": "5e730e8e0b852a417aa49ceb",
        "name": "test",
        "organization": "ЧП «test test»",
        "address": "",
        "business_id": "5e730e740b852a417aa49cea",
        "epos": {
          "merchantId": "106600000050000",
          "terminalId": "20660000"
        },
        "date": 1584598670296,
        "logo": null,
        "type": {
          "ru": "Internet",
          "uz": "Internet"
        },
        "terms": null
      },
      "meta": {
        "source": "subscribe",
        "owner": "5e730e8e0b852a417aa49ceb",
        "source_cancel": "subscribe"
      },
      "processing_id": null
    }
  ]
}
```
