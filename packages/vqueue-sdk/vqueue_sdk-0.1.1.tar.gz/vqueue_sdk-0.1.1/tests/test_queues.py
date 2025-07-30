import pytest
import requests

from vqueue.exceptions import VQueueApiError, VQueueError, VQueueNetworkError
from vqueue.queues import TokenVerifier

INVALID_TOKEN = "invalid1-f37d-499f-b30d-7542a7b4f5db"
VALID_TOKEN_SUCCESS_TRUE = "f1a10b71-f37d-499f-b30d-7542a7b4f5db"
VALID_TOKEN_SUCCESS_FALSE = "b184ffee-6c23-4951-a8b3-9fb3769d48e4"
BAD_JSON_RESPONSE_TOKEN = "ec3884e7-4896-466c-b4be-5105bcc6d2aa"
BAD_FORMAT_RESPONSE_TOKEN = "45cd2352-7c48-4ead-8721-b0cf49f97018"
NETWORK_ERROR_TOKEN = "f93243c4-8fdd-46d8-aa68-7a8967c5d3c8"


class MockResponse:
    """Mock response from requests' request"""

    def __init__(self, token: str):
        self.token = token
        self.status_code = (
            200
            if token
            in [
                VALID_TOKEN_SUCCESS_TRUE,
                BAD_FORMAT_RESPONSE_TOKEN,
            ]
            else 404
        )

    def json(self):
        if self.token == VALID_TOKEN_SUCCESS_TRUE:
            return {
                "data": {
                    "token": VALID_TOKEN_SUCCESS_TRUE,
                    "finished_line": {"finished_at": "2024-09-17T09:47:10Z", "ingressed_at": "2024-09-17T09:15:53Z"},
                },
                "message": "Token succesfully verified",
                "success": True,
            }

        if self.token == VALID_TOKEN_SUCCESS_FALSE:
            return {
                "data": {},
                "message": "The queue could not be verified.",
                "success": False,
                "error_code": 404,
            }

        if self.token == BAD_JSON_RESPONSE_TOKEN:
            raise requests.JSONDecodeError(
                "Bad JSON",
                "",
                0,
            )

        if self.token == BAD_FORMAT_RESPONSE_TOKEN:
            return {
                "success": True,
            }


class MockSession:
    """Mock requests.Session()"""

    def get(self, url: str):
        """Mock Session().get method"""

        # BASE_URL/verify?token={token}
        token = url[url.find("token=") + 6 :]

        if token == NETWORK_ERROR_TOKEN:
            raise requests.exceptions.RequestException()

        return MockResponse(token)

    def close(self):
        pass


def test_raises_for_invalid_uuid():
    # Act & Assert
    with pytest.raises(ValueError):
        TokenVerifier().verify_token(INVALID_TOKEN)


def test_raises_for_network_error(monkeypatch):
    # Arrange
    monkeypatch.setattr(requests, "Session", MockSession)

    # Act & Assert
    with pytest.raises(VQueueNetworkError):
        TokenVerifier().verify_token(NETWORK_ERROR_TOKEN)


def test_raises_for_invalid_json_response(monkeypatch):
    # Arrange
    monkeypatch.setattr(requests, "Session", MockSession)

    # Act & Assert
    with pytest.raises(VQueueError, match="Invalid JSON response"):
        TokenVerifier().verify_token(BAD_JSON_RESPONSE_TOKEN)


def test_raises_for_bad_format_in_response(monkeypatch):
    # Arrange
    monkeypatch.setattr(requests, "Session", MockSession)

    # Act & Assert
    with pytest.raises(VQueueError, match="Bad format"):
        TokenVerifier().verify_token(BAD_FORMAT_RESPONSE_TOKEN)


def test_raises_for_api_error_code(monkeypatch):
    # Arrange
    monkeypatch.setattr(requests, "Session", MockSession)

    # Act & Assert
    with pytest.raises(VQueueApiError):
        TokenVerifier().verify_token(VALID_TOKEN_SUCCESS_FALSE)


def test_valid_token_response(monkeypatch):
    # Arrange
    monkeypatch.setattr(requests, "Session", MockSession)

    # Act
    verification_result = TokenVerifier().verify_token(VALID_TOKEN_SUCCESS_TRUE)

    # Assert
    assert verification_result.success is True
    assert verification_result.message == "Token succesfully verified"
    assert verification_result.data is not None
    assert verification_result.data.token == VALID_TOKEN_SUCCESS_TRUE
