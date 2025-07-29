from rest_framework.exceptions import ErrorDetail
from django.conf import settings
from importlib import import_module

import logging

logger = logging.getLogger(__name__)


def flatten_errors(error_data):
    """
    Flattens nested error data into a list of error messages.

    This utility function recursively traverses the given error_data,
    extracting error messages from lists, dictionaries, and ErrorDetail instances.

    Args:
        error_data: The error data to be flattened, which can be a list,
                    dictionary, or ErrorDetail object.

    Returns:
        A list of strings representing the extracted error messages.
    """

    def extract_messages(data):
        if isinstance(data, list):
            messages = []
            for item in data:
                messages.extend(extract_messages(item))
            return messages
        elif isinstance(data, dict):
            messages = []
            for value in data.values():
                messages.extend(extract_messages(value))
            return messages
        elif isinstance(data, ErrorDetail):
            return [str(data)]
        else:
            return [str(data)]

    return extract_messages(error_data)


def get_configured_base_exception_class():
    """
    Retrieves the custom base exception class configured in settings.

    This function retrieves the custom base exception class configured in
    settings via the CUSTOM_BASE_EXCEPTION setting. If the setting is not
    present, it returns None.

    Args:
        None

    Returns:
        The custom base exception class if it is configured in settings,
        otherwise None.
    """
    path = getattr(settings, "CUSTOM_BASE_EXCEPTION", None)
    if not path:
        return None

    try:
        module_path, class_name = path.rsplit(".", 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except Exception as e:
        logger.warning(f'Could not import CUSTOM_BASE_EXCEPTION: "{path}": {e}')
        return None
