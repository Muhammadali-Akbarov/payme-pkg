from django.conf import settings


def get_params(params: dict) -> dict:
    """
    Use this function to get the parameters from the payme.
    """
    account: dict = params.get("account")

    clean_params: dict = {}
    clean_params["_id"] = params.get("id")
    clean_params["time"] = params.get("time")
    clean_params["amount"] = params.get("amount")
    clean_params["reason"] = params.get("reason")
    clean_params["from"] = params.get("from")
    clean_params["to"] = params.get("to")

    if account is not None:
        account_name: str = settings.PAYME.get("PAYME_ACCOUNT")
        clean_params["order_id"] = account[account_name]

    return clean_params
