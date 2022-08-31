# Integration Payme API with Python | Payment Service 
Sourcode and Resources for Python & Payme <hr>
Support Telegram - http://t.me/Muhammadalive <br>
Documentation & More https://developer.help.paycom.uz/ru/
<hr>

## Getting started
There are two ways to install the library:

* Installation using pip (a Python package manager):

```
$ pip install payme-pkg==1.3
```
* Installation from source (requires git):

```
$ git clone https://github.com/Muhammadali-Akbarov/payme_pkg
$ cd payme_pkg
$ python setup.py install
```
or:
```
$ pip install git+https://github.com/Muhammadali-Akbarov/payme_pkg
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
  * [Subscribe Cards](#subscribe-cards)
    * [Cards Create](#cards-create)
    * [Cards Get Verify Code](#cards-get-verify-code)
    * [Cards Verify](#cards-verify)
    * [Cards Check](#cards-check)
    * [Cards Remove](#cards-remove)
   
  * [Subscribe Receipts](#subscribe-receipts)
    * [Receipts Create](#receipts-create)
    * [Receipts Create P2P](#receipts-create-p2p)
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

from lib.payme.cards.subscribe_cards import PaymeSubscribeCards


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
{'jsonrpc': '2.0',
 'result': {
    'card': {
        'expire': '03/99',
        'number': '860006******6311',
        'recurrent': True,
        'token': '630e5ffdd15d8d8d093b379b_2fsaoABWafecn20kofV4PFafFZjeGDWS9adM1PmboQaEZbbaxMcnaskctMbU9Iv8qgrOuKGz8SnjvZvYXDK64m1eS9gA5jZ7BBRaQybMXrDPtFPJ1fwek5B1KoIv5cMiCWYXj7ezpYEdJAKTIQw0Np9HsTXjqco4gQG3m8MOfeH9ovkdm66O6yj45oKXRmJyAK5i0SchXNNomACH3Oq80KyoRE1VoBRxvoKyMkOx0xcepXovxK9d3v26a8z7UtyokwY33N8MupviM3A5WHB5Xh35WZJJyFnxTSi1vvnYnG7uVd6Bb1GjV2yAHnimss8aEZGW5V7ZiPrhf8r6WJAeHciYDGK3msRKZJBQTfjgOdE9tGrEnMezVkxr1JXX0xSn5qqec2',
        'type': '22618',
        'verify': False
        }
    }
}
```

## Cards Get Verify Code
Example for cards create method for to generate token from card:
* Request
```
from pprint import pprint

from lib.payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._card_get_verify_code(
    token="630e5ffdd15d8d8d093b379b_2fsaoABWafecn20kofV4PFafFZjeGDWS9adM1PmboQaEZbbaxMcnaskctMbU9Iv8qgrOuKGz8SnjvZvYXDK64m1eS9gA5jZ7BBRaQybMXrDPtFPJ1fwek5B1KoIv5cMiCWYXj7ezpYEdJAKTIQw0Np9HsTXjqco4gQG3m8MOfeH9ovkdm66O6yj45oKXRmJyAK5i0SchXNNomACH3Oq80KyoRE1VoBRxvoKyMkOx0xcepXovxK9d3v26a8z7UtyokwY33N8MupviM3A5WHB5Xh35WZJJyFnxTSi1vvnYnG7uVd6Bb1GjV2yAHnimss8aEZGW5V7ZiPrhf8r6WJAeHciYDGK3msRKZJBQTfjgOdE9tGrEnMezVkxr1JXX0xSn5qqec2"
)
```
* Response
```
{'jsonrpc': '2.0',
 'result': {
    'phone': '99890*****66', 
    'sent': True, 
    'wait': 60000
    }
}
```

## Cards Verify
Example for cards create method for to generate token from card:
* Request
```
from pprint import pprint

from lib.payme.cards.subscribe_cards import PaymeSubscribeCards


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
{'jsonrpc': '2.0',
 'result': {
    'card': {
        'expire': '03/99',
        'number': '860006******6311',
        'recurrent': True,
        'token': '630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p',
        'type': '22618',
        'verify': True
        }
    }
}
```

## Cards Check
Example for cards create method for to generate token from card:
* Request
```
from pprint import pprint

from lib.payme.cards.subscribe_cards import PaymeSubscribeCards


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
{'jsonrpc': '2.0',
 'result': {
    'card': {
        'expire': '03/99',
        'number': '860006******6311',
        'recurrent': True,
        'token': '630e691fd15d8d8d093b379c_70mKyzqS8d1wTWzovIGjt9dKmjpn1KI8Y9XakPrfpbUASTBaZYbC1DjDcjYRmuNJep9gZrTRtHyEGBQYmBaPufuozF51bv4qEPsQnodq1VcD7tYyREwUXjMXXZUeu7Ek0REQCekCvVHX6rtNBpb4vtViJoNVjp94XpTqu0Bn3yYYb0CHu951wFydzRsieGxjGNrvx1oKyBcq0CdOUwoffRIt2VPvx5R2aVmc6ahwyhn387FEEcpO1PnjIJkWKTBWdI35ZPQnb1u1oss5aPg06E279THXRkoTThixbeqiD2JkWSXweNVGGDhTS30V4j61G3NWEPO2H3k4uFmCjjIQSzx4TxKzUgHg1i2q953PRUGjT4JZBRHMDxaN5tWuctEMNmY06p',
        'type': '22618',
        'verify': True
        }
    }
}
```
## Cards Remove
Example for cards create method for to generate token from card:
* Request
```
from pprint import pprint

from lib.payme.cards.subscribe_cards import PaymeSubscribeCards


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
{'jsonrpc': '2.0',
 'result': {
     'success': True
    }
}
```
