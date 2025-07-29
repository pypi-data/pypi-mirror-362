import uuid
import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    ObjectDoesNotExist,
)
from django.db import IntegrityError
from django.conf import settings

from .utils import flatten_errors, get_configured_base_exception_class

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework (DRF).

    This function ensures all error responses follow a consistent structure:
        {
            "status": False,
            "message": [<list of error messages>],
            "code": <optional error code>,
            "error_id": <optional UUID for internal tracking>
        }

    Features:
    - Re-formats manually returned DRF Response objects into the standard format.
    - Delegates to DRF's default exception handler when applicable.
    - Handles project-specific base exceptions dynamically (based on settings.CUSTOM_BASE_EXCEPTION).
    - Gracefully handles Django and DB-specific errors such as ValidationError, ObjectDoesNotExist, and IntegrityError.
    - Logs and formats unhandled exceptions with a unique error ID and optional stack trace (shown in DEBUG mode).

    Args:
        exc (Exception): The raised exception instance.
        context (dict): Extra context about the request, including view and request objects.

    Returns:
        Response: A DRF Response object with a standardized error payload.
    """

    # If the exception is a manually returned Response, reformat it
    if isinstance(exc, Response):
        return Response(
            {"status": False, "message": flatten_errors(exc.data)},
            status=exc.status_code,
        )

    # Call DRF's default exception handler
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {"status": False, "message": flatten_errors(response.data)}
        return response

    BaseExceptionClass = get_configured_base_exception_class()
    if BaseExceptionClass and isinstance(exc, BaseExceptionClass):
        logger.warning(f"Project Base Exception: {exc.message} (Code: {exc.code})")
        return Response(
            {
                "status": False,
                "message": [exc.message],
                "code": exc.code,
            },
            status=exc.status_code,
        )

    # Handle Django ValidationError explicitly
    if isinstance(exc, DjangoValidationError):
        return Response({"status": False, "message": [str(exc)]}, status=400)

    # Handle missing objects explicitly (instead of Django returning a raw 500 error)
    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"status": False, "message": ["Requested object not found."]}, status=404
        )

    # Handle database integrity errors (e.g., unique constraint violations)
    if isinstance(exc, IntegrityError):
        return Response(
            {"status": False, "message": ["Database integrity error."]}, status=400
        )

    # Handle unexpected Python exceptions
    if not response:
        error_id = str(uuid.uuid4())
        logger.error(f"[Error ID: {error_id}] Unhandled exception", exc_info=True)

        if settings.DEBUG:
            # Show full error details in DEBUG mode
            import traceback

            detailed_error = traceback.format_exc()
            message = [f"Error ID: {error_id}", detailed_error]
        else:
            # Show a generic error message in non-DEBUG mode
            message = [
                f"Something went wrong. Please share this error ID with support: {error_id}"
            ]

        return Response(
            {
                "status": False,
                "message": message,
                "error_id": error_id,
            },
            status=500,
        )
