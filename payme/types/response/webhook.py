import typing as t
from dataclasses import dataclass, field


class CommonResponse:
    """
    The common response structure
    """

    def as_resp(self):
        response = {"result": {}}
        for key, value in self.__dict__.items():
            response["result"][key] = value
        return response


@dataclass
class Shipping(CommonResponse):
    """
    Shipping information response structure
    """

    title: str
    price: int


@dataclass
class Item(CommonResponse):
    """
    Item information response structure
    """

    discount: int
    title: str
    price: int
    count: int
    code: str
    units: int
    vat_percent: int
    package_code: str

    def as_resp(self):
        return {
            "discount": self.discount,
            "title": self.title,
            "price": self.price,
            "count": self.count,
            "code": self.code,
            "units": self.units,
            "vat_percent": self.vat_percent,
            "package_code": self.package_code,
        }


@dataclass
class CheckPerformTransaction(CommonResponse):
    """
    Receipt information response structure for transaction checks.
    """

    allow: bool
    additional: t.Optional[t.Dict[str, str]] = None
    receipt_type: t.Optional[int] = None
    shipping: t.Optional[Shipping] = None
    items: t.List[Item] = field(default_factory=list)

    def add_item(self, item: Item):
        self.items.append(item)

    def as_resp(self):
        detail_dict = {}
        receipt_dict = {"allow": self.allow}

        if self.additional:
            receipt_dict["additional"] = self.additional

        if isinstance(self.receipt_type, int):
            detail_dict["receipt_type"] = self.receipt_type

        if self.shipping:
            detail_dict["shipping"] = self.shipping.as_resp()

        if self.items:
            detail_dict["items"] = [item.as_resp() for item in self.items]

        if detail_dict:
            receipt_dict["detail"] = detail_dict

        return {"result": receipt_dict}


@dataclass
class CreateTransaction(CommonResponse):
    """
    The create transaction request
    """

    transaction: str
    state: str
    create_time: int


@dataclass
class PerformTransaction(CommonResponse):
    """
    The perform transaction response
    """

    transaction: str
    state: str
    perform_time: int


@dataclass
class CancelTransaction(CommonResponse):
    """
    The cancel transaction request
    """

    transaction: str
    state: str
    cancel_time: str


@dataclass
class CheckTransaction(CommonResponse):
    """
    The check transaction request
    """

    transaction: str
    state: str
    reason: str
    create_time: int
    perform_time: t.Optional[int] = None
    cancel_time: t.Optional[int] = None


@dataclass
class GetStatement(CommonResponse):
    """
    The check perform transactions response
    """

    transactions: t.List[t.Dict[str, str | int | t.Dict[str, str | int]]]


@dataclass
class SetFiscalData(CommonResponse):
    """
    The set fiscal data request
    """

    success: bool
