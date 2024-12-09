import requests

from payme.exceptions import general as exc


networking_errors = (
    requests.exceptions.Timeout,
    requests.exceptions.HTTPError,
    requests.exceptions.ConnectionError,
    requests.exceptions.TooManyRedirects,
    requests.exceptions.URLRequired,
    requests.exceptions.MissingSchema,
    requests.exceptions.InvalidURL,
    requests.exceptions.InvalidHeader,
    requests.exceptions.JSONDecodeError,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ReadTimeout,
    requests.exceptions.SSLError,
    requests.exceptions.ProxyError,
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.StreamConsumedError,
    requests.exceptions.RequestException
)


class HttpClient:
    """
    A simple HTTP client to handle requests to a specified URL.
    It provides methods for sending GET, POST, PUT, and DELETE requests
    with error handling.
    """

    def __init__(self, url: str, headers: dict = None):
        """
        Initialize the HttpClient.

        Parameters
        ----------
        url : str
            The base URL for the API (e.g., 'https://checkout.paycom.uz/api').
        headers : dict, optional
            Optional default headers to include in all requests.
            These headers will be sent with every request unless overridden.
        """
        self.url = url
        self.headers = headers

    def post(self, json: dict, timeout: int = 10):
        """
        Send a POST request to the specified URL with the provided JSON data.

        Parameters
        ----------
        json : dict
            The JSON data payload for the POST request. This will be sent
            as the request body.
        timeout : int, optional
            The request timeout duration in seconds (default is 10 seconds).

        Returns
        -------
        dict
            A dictionary containing the response data if the request was
            successful, or an error message if an error occurred.
        """
        try:
            response = requests.post(
                url=self.url,
                headers=self.headers,
                json=json,
                timeout=timeout
            )
            response.raise_for_status()
            response_data = response.json()

            # Check if the response contains a specific error format
            if "error" in response_data:
                return self.handle_payme_error(response_data["error"])

            return response_data

        except networking_errors as exc_data:
            raise exc.PaymeNetworkError(data=exc_data)

    def handle_payme_error(self, error: dict):
        """
        Handle Paycom-specific errors from the JSON-RPC error response.

        Parameters
        ----------
        error : dict
            The error dictionary from Paycom's response, typically containing
            error details such as code, message, and data.

        Returns
        -------
        None
            Raises an exception based on the error code received from
            Paycom's response.
        """
        error_code = error.get("code", "Unknown code")
        error_message = error.get("message", "Unknown error")
        error_data = error.get("data", "")

        exception_class = exc.errors_map.get(error_code, exc.BaseError)
        exception_class.message = error_message

        if exception_class == exc.BaseError:
            raise exc.BaseError(code=error_code, message=error_message)

        raise exception_class(data=error_data)
