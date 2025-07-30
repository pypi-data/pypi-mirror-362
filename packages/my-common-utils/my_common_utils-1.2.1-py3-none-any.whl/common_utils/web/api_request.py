import requests
from requests import Response, RequestException
import json
from pydantic import HttpUrl
from typing import Literal, Any



from common_utils.logger import create_logger

log = create_logger("Request Helper")


def safe_request(
        method: Literal['GET', 'PUT', 'POST'],
        url: HttpUrl,
        headers: dict[str, str] | None = None,
        data: Any | None = None,
        params: dict | None = None,
        catch_exception: bool | None = False
) -> dict | None:
    """
    Send a GET request to the given URL with the given data and headers.

    Arguments:
        method: The request method to use
        url: Url to send the request to
        headers: Http headers to send with the request
        data: Payload data to send
        params: Url parameters
        catch_exception: If exceptions shall be raised or not

    Raises:

    """
    final_headers = {"Content-Type": "application/json"}
    try:
        if headers:
            final_headers.update(headers)
        response: Response = requests.request(
            method=method,
            url=url,
            headers=final_headers,
            json=data,
            params=params
        )
        response.raise_for_status()
        return response.json()

    except (RequestException, ValueError):
        if catch_exception:
            return None
        raise



def get_request(
        url: HttpUrl,
        headers: dict[str, str] | None = None,
        catch_exception: bool | None = False
) -> dict | None:
    """
    Send a GET request to the given URL with the given data and headers.

    Arguments:
        url: Url to send the request to
        headers: Http headers to send with the request
        catch_exception: If exceptions shall be raised or not

    Raises:
       RequestException, ValueError
    """
    return safe_request(method='GET', url=url, headers=headers, catch_exception=catch_exception)


def post_request(url: HttpUrl, payload: dict, headers=None, raise_exception=False) -> dict | None:
    """
    Send a GET request to the given URL with the given data and headers.

    Arguments:
        url: Url to send the request to
        headers: Http headers to send with the request
        payload: Data payload to send with the request
        raise_exception: If exceptions shall be raised or not

    Raises:
       RequestException, ValueError
    """

    return safe_request(method='POST', url=url, data=payload, headers=headers, catch_exception=raise_exception)

