from pathlib import Path

import requests

from ._config import API_BASE_PATH
from .exceptions import VQueueApiError, VQueueError, VQueueNetworkError
from .types import VerificationResult, VerificationResultData
from .utils import validate_uuidv4

QUEUES_API_URL = Path(API_BASE_PATH).joinpath("queue/")
VERIFY_API_URL = QUEUES_API_URL.joinpath("verify")


class TokenVerifier:
    """Client to verify Virtual Queue tokens"""

    def __init__(self):
        """Initialize the TokenVerifier with a network session"""
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def verify_token(self, token: str) -> VerificationResult:
        """Verify the given token and return the data related to the queue.

        Args:
            token: The token to be verified.

        Returns:
            Verified token data.

        Raises:
            ValueError: If the token is not a valid UUIDv4 string.
            VQueueNetworkError: If there is a notworking related error.
            VQueueApiError: If the API responds with an error status.
            VQueueError: For unexpected API-related errors.
        """

        uuid_token = validate_uuidv4(token)

        try:
            response = self.session.get(f"{VERIFY_API_URL}?token={uuid_token}")
            response_data = response.json()
        except requests.JSONDecodeError as e:
            raise VQueueError("Invalid JSON response") from e
        except requests.exceptions.RequestException as e:
            raise VQueueNetworkError from e

        if 200 <= response.status_code < 300:
            if response_data["success"]:
                try:
                    return VerificationResult(
                        success=True,
                        message=response_data["message"],
                        data=VerificationResultData(
                            token=response_data["data"]["token"],
                            ingressed_at=response_data["data"]["finished_line"]["ingressed_at"],
                            finished_at=response_data["data"]["finished_line"]["finished_at"],
                        ),
                    )
                except Exception as e:
                    raise VQueueError("Bad format in response") from e

            raise VQueueError("HTTP response is OK, but the body `success` field is not `True`.")

        raise VQueueApiError(
            response.status_code,
            response_data["message"],
            response_data["error_code"],
            response_data["data"],
        )
