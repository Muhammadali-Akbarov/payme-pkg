# Integration Payme API with Python | Payment Service 
Sourcode and Resources for Python & Payme <hr>
Support Telegram - http://t.me/Muhammadalive <br>
Documentation & More https://developer.help.paycom.uz/ru/ <br>
Video Documentation & More https://www.youtube.com/watch?v=sJORIyykHcw
<hr>

## Getting started
There are two ways to install the library:

* Installation using pip (a Python package manager):

```
$ pip install payme-pkg
```
* Installation from source (requires git):

```
$ git clone https://github.com/Muhammadali-Akbarov/payme-pkg
$ cd payme-pkg
$ python setup.py install
```
or:
```
$ pip install git+https://github.com/Muhammadali-Akbarov/payme-pkg
```

### Library Structure
```
payme
    ├── cards
    │   ├── __init__.py
    │   └── subscribe_cards.py
    ├── __init__.py
    └── receipts
        ├── __init__.py
        └── subscribe_receipts.py
```
### Test Cards
```
Card Numer: 8600 4954 7331 6478 Expire Date: 03/99 SMS Code: 666666 
Card Numer: 8600 0691 9540 6311 Expire Date: 03/99 SMS Code: 666666 
```

## Contents

  * [Getting Started](#getting-started)
  * Subscribe Cards
    * [Cards Create](#cards-create)
    * [Cards Get Verify Code](#cards-get-verify-code)
    * [Cards Verify](#cards-verify)
    * [Cards Check](#cards-check)
    * [Cards Remove](#cards-remove)
   
  * Subscribe Receipts
    * [Receipts Create](#receipts-create)
    * [Receipts Pay](#receipts-pay)
    * [Receipts Send](#receipts-send)
    * [Receipts Cancel](#receipts-cancel)
    * [Receipts Check](#receipts-check)
    * [Receipts Get](#receipts-get)
    * [Receipts Get All ](#receipts-get-all)
## Cards Create
Example for cards create method for to generate token from card:

* Request

```
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._cards_create(
    number="8600069195406311",
    expire="0399",
    save=True,
)

pprint(resp)
```
* Response

```
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
* Request
```
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._card_get_verify_code(
    token="630e5ffdd15d8d8d093b379b_2fsaoABWafecn20kofV4PFafFZjeGDWS9adM1PmboQaEZbbaxMcnaskctMbU9Iv8qgrOuKGz8SnjvZvYXDK64m1eS9gA5jZ7BBRaQybMXrDPtFPJ1fwek5B1KoIv5cMiCWYXj7ezpYEdJAKTIQw0Np9HsTXjqco4gQG3m8MOfeH9ovkdm66O6yj45oKXRmJyAK5i0SchXNNomACH3Oq80KyoRE1VoBRxvoKyMkOx0xcepXovxK9d3v26a8z7UtyokwY33N8MupviM3A5WHB5Xh35WZJJyFnxTSi1vvnYnG7uVd6Bb1GjV2yAHnimss8aEZGW5V7ZiPrhf8r6WJAeHciYDGK3msRKZJBQTfjgOdE9tGrEnMezVkxr1JXX0xSn5qqec2"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._cards_verify(
    verify_code="666666",
    token="630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._cards_check(
    token="630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._cards_check(
    token="630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p"
)

pprint(resp)
```
* Response
```
{
  "jsonrpc": "2.0",
  "result": {
    "success": true
  }
}
```
## Receipts Create
Example for receipts create method:
* Request
```
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._receipts_create(
    amount=10000,
    order_id="1"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._receipts_pay(
    invoice_id="631186b6c4420cbf2712a243",
    token="63118a5dd15d8d8d093b37b7_X2j34OIJPnROfsgzYZCZ0w7OcC50zzwiowTsotEVO1uUbxkzaDrvdOno6jicQTrcRmxvibxrye4vUS3AynTNPaPCTGpfk3RCKmT9NaOAyyTmctAjWsjwvqGR5XUzAP1Xcx12GkhuQi6VJ4BeaIXOokSRu06rRjaivmJQ8HTiJiR9b3OmZtrhkIRNcNXnnp9zYm1mFP4BuqGpS8BMnY0ASIE6ffxWykjgBcDTAfWBFt4mg7O9Dsvx0aj3IB8z3RIbZYtDZJnUVhCZrwW7ONVI9uEAdxNthorjO6PbV7TQ8XCjrztgGf6uCtOwwxasiIUVZN6tCVDk8A8NvVSUzUHXQHVkaPn5heJNa3K4WsffIckq7SwMbiw3UbawipeZKyD3iwk1Km",
    phone="998901304527"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._receipts_send(
    invoice_id="631186b6c4420cbf2712a243",
    phone="998901304527"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._receipts_cancel(
    invoice_id="63119303c4420cbf2712a245"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._receipts_check(
    invoice_id="63119303c4420cbf2712a245"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._reciepts_get(
    invoice_id="6311946bc4420cbf2712a247"
)

pprint(resp)
```
* Response
```
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
* Request
```
from pprint import pprint

from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._reciepts_get_all(
    count=2,
    _from=1636398000000,
    to=1636398000000,
    offset=0
)

pprint(resp)
```
* Response
```
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
