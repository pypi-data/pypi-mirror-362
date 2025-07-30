from functools import wraps
from typing import Callable, Optional

import httpx

from labtasker.api_models import BaseResponseModel
from labtasker.client.core.config import get_client_config
from labtasker.client.core.exceptions import (
    LabtaskerConnectError,
    LabtaskerConnectTimeout,
    LabtaskerHTTPStatusError,
    LabtaskerNetworkError,
)
from labtasker.client.core.logging import stderr_console, stdout_console
from labtasker.client.core.paths import get_labtasker_client_config_path

server_notification_prefix = {
    "info": "[bold dodger_blue1]INFO(notification):[/bold dodger_blue1] ",
    "warning": "[bold orange1]WARNING(notification):[/bold orange1] ",
    "error": "[bold red]ERROR(notification):[/bold red] ",
}

server_notification_level = {
    "low": 0,
    "medium": 1,
    "high": 2,
}


def display_server_notifications(
    func: Optional[Callable[..., "BaseResponseModel"]] = None, /
):
    def decorator(function: Callable[..., "BaseResponseModel"]):
        @wraps(function)
        def wrapped(*args, **kwargs):
            resp = function(*args, **kwargs)

            level = "medium"
            if get_labtasker_client_config_path().exists():
                level = get_client_config().display_server_notifications_level

            enabled = level != "none"

            if not enabled:
                return resp

            notifications = resp.notification or []
            for n in notifications:
                if (
                    server_notification_level[n.level]
                    < server_notification_level[level]
                ):  # skip if level is lower than the config
                    continue
                out = stdout_console if n.type == "info" else stderr_console
                out.print(
                    server_notification_prefix[n.type] + n.details,
                )

            return resp

        return wrapped

    if func is not None:
        return decorator(func)

    return decorator


def cast_http_error(func: Optional[Callable] = None, /):
    def decorator(function: Callable):
        @wraps(function)
        def wrapped(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except httpx.HTTPStatusError as e:
                raise LabtaskerHTTPStatusError(
                    message=str(e), request=e.request, response=e.response
                ) from e
            except httpx.ConnectError as e:
                raise LabtaskerConnectError(message=str(e), request=e.request) from e
            except httpx.ConnectTimeout as e:
                raise LabtaskerConnectTimeout(message=str(e), request=e.request) from e
            except httpx.HTTPError as e:
                raise LabtaskerNetworkError(str(e)) from e

        return wrapped

    if func is not None:
        return decorator(func)

    return decorator


def raise_for_status(r: httpx.Response) -> httpx.Response:
    """
    Call the original raise_for_status but preserve detailed error information.

    Args:
        r: The httpx.Response object

    Returns:
        The original response if successful

    Raises:
        HTTPStatusError: Enhanced with more detailed error information
    """
    try:
        return r.raise_for_status()
    except httpx.HTTPStatusError as e:
        error_details = r.text
        enhanced_message = f"{str(e)}\nResponse details: {error_details}"
        raise httpx.HTTPStatusError(
            enhanced_message, request=e.request, response=e.response
        ) from None
