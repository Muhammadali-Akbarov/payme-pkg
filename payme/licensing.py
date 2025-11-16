import os
from typing import Optional

import requests

from payme.exceptions.general import UnknownPartnerError


FREE_API_KEY = "6bb7d17e-c22b-44ee-96f3-d93f8b0d750b"
API_KEY_ENV_NAME = "PAYTECH_API_KEY"


def _get_api_key(explicit_key: Optional[str]) -> str:
    api_key = explicit_key or os.environ.get(API_KEY_ENV_NAME)
    if not api_key:
        raise UnknownPartnerError(
            "Missing api_key for payme-pkg. To get a valid api_key please contact @muhammadali_me on Telegram."
        )
    return api_key


def validate_api_key(api_key: Optional[str] = None) -> None:
    key = _get_api_key(api_key)

    if key == FREE_API_KEY:
        return

    try:
        license_url = "https://api.pay-tech.uz"
        response = requests.post(
            license_url,
            json={"api_key": key},
            timeout=5,
        )
    except requests.RequestException as exc:
        raise UnknownPartnerError(
            "Unable to validate api_key. Please contact @muhammadali_me on Telegram."
        ) from exc

    if response.status_code != 200:
        raise UnknownPartnerError(
            "Invalid api_key for payme-pkg. Please contact @muhammadali_me on Telegram."
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise UnknownPartnerError(
            "License server returned invalid response. Please contact @muhammadali_me on Telegram."
        ) from exc

    if not payload.get("valid", False):
        raise UnknownPartnerError(
            "Invalid or inactive api_key for payme-pkg. To get access please contact @muhammadali_me on Telegram."
        )
