from dataclasses import dataclass
from typing import Dict, Optional, Union


class Common:
    """
    The common response structure.
    """
    jsonrpc: str
    id: int

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Prepare fields for nested dataclasses
        """
        field_values = {}
        for field in cls.__dataclass_fields__:
            field_type = cls.__dataclass_fields__[field].type
            field_data = data.get(field)

            if isinstance(field_data, dict) and issubclass(field_type, Common):
                field_values[field] = field_type.from_dict(field_data)
            else:
                field_values[field] = field_data

        return cls(**field_values)


@dataclass
class Account(Common):
    """
    The account object represents a user's banking account.
    """
    _id: str
    account_number: str
    account_name: str
    account_type: str
    bank_name: str
    currency: str
    status: str


@dataclass
class PaymentMethod(Common):
    """
    The payment method object represents a user's payment method.
    """
    name: str
    title: str
    value: str
    main: Optional[bool] = None


@dataclass
class Detail(Common):
    """
    The detail object represents additional details for a receipt.
    """
    discount: Optional[str] = None
    shipping: Optional[str] = None
    items: Optional[str] = None


# pylint: disable=C0103
@dataclass
class MerchantEpos(Common):
    """
    The merchantEpos object represents a user's ePOS.
    """
    eposId: str
    eposName: str
    eposType: str
    eposTerminalId: str


@dataclass
class Meta(Common):
    """
    The meta object represents additional metadata for a receipt.
    """
    source: any = None
    owner: any = None
    host: any = None


@dataclass
class Merchant:
    """
    The merchant object represents a user's merchant.
    """
    _id: str
    name: str
    organization: str
    address: Optional[str] = None
    business_id: Optional[str] = None
    epos: Optional[MerchantEpos] = None
    restrictions: Optional[str] = None
    date: Optional[int] = None
    logo: Optional[str] = None
    type: Optional[str] = None
    terms: Optional[str] = None


@dataclass
class Payer(Common):
    """
    The payer object represents a user's payer.
    """
    phone: str


@dataclass
class Receipt(Common):
    """
    The receipt object represents a payment receipt.
    """
    _id: str
    create_time: int
    pay_time: int
    cancel_time: int
    state: int
    type: int
    external: bool
    operation: int
    category: any = None
    error: any = None
    description: str = None
    detail: Detail = None
    currency: int = None
    commission: int = None
    card: str = None
    creator: str = None
    payer: Payer = None
    amount: Union[float, int] = None
    account: list[Account] = None
    merchant: Merchant = None
    processing_id: str = None
    meta: Meta = None


@dataclass
class CreateResult(Common):
    """
    The result object for the create response.
    """
    receipt: Receipt


@dataclass
class CreateResponse(Common):
    """
    The create response structure.
    """
    result: CreateResult


@dataclass
class PayResponse(CreateResponse):
    """
    The pay response structure.
    """


@dataclass
class SendResult(Common):
    """
    The result object for the send response.
    """
    success: bool


@dataclass
class SendResponse(Common):
    """
    The send response structure.
    """
    result: SendResult


@dataclass
class CancelResponse(CreateResponse):
    """
    The cancel response structure.
    """


@dataclass
class CheckResult(Common):
    """
    The result object for the check response.
    """
    state: int


@dataclass
class CheckResponse(Common):
    """
    The check response structure.
    """
    result: CheckResult


@dataclass
class GetResponse(CreateResponse):
    """
    The result object for the get response.
    """


@dataclass
class GetAllResponse(Common):
    """
    The result object for the get all response.
    """
    result: list[Receipt] = None
