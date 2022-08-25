# Integration Payme API with Python | Payment Service 
Sourcode and Resources for Python & Payme <hr>
Support Telegram - http://t.me/Muhammadalive <br>
Documentation & More https://developer.help.paycom.uz/ru/
<hr>

## Getting started
There are two ways to install the library:

* Installation using pip (a Python package manager):

```
$ pip install payme-pkg==1.2
```
* Installation from source (requires git):

```
$ git clone https://github.com/Muhammadali-Akbarov/payme_pkg
$ cd payme_uz
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

## Contents

  * [Getting Started](#getting-started)
  * [Subscribe Cards](#subscribe-cards)
    * [Cards Create](#cards-create)
    * [Card Get Verify Code](#card-get-verify-code)
    * [Card Verify](#card-verify)
    * [Card Check](#card-check)
    * [Card Remove](#card-remove)
   
  * [Subscribe Receipts](#subscribe-receipts)
    * [Receipts Create](#receipts-create)
    * [Receipts Create P2P](#receipts-create-p2p)
    * [Receipts Pay](#receipts-pay)
    * [Receipts Send](#receipts-send)
    * [Receipts Cancel](#receipts-cancel)
    * [Receipts Check](#receipts-check)
    * [Receipts Get](#receipts-get)
    * [Receipts Get All ](#receipts-get-all)
