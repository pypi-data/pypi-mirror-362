from unittest.mock import patch, MagicMock

import pytest
import requests

from sklik.api import sklik_request, _handle_response, SklikApi
from sklik.exception import SklikException
from sklik.util import SKLIK_API_URL


# ========= Tests for _handle_response =========

def test_handle_response_success():
    # Create a fake response with status 200.
    response = MagicMock(spec=requests.Response)
    response.json.return_value = {"status": 200, "data": "some data"}

    result = _handle_response(response)
    assert result == {"status": 200, "data": "some data"}


def test_handle_response_error():
    # Create a fake response with a non-200 status.
    response = MagicMock(spec=requests.Response)
    response.url = "https://example.com/api"
    response.json.return_value = {
        "status": 400,
        "statusMessage": "Bad arguments"
    }

    with pytest.raises(SklikException) as exc_info:
        _handle_response(response)

    exc = exc_info.value
    assert "Could not request https://example.com/api" in str(exc)
    assert exc.status_code == 400
    assert exc.additional_information == "Bad arguments"


# ========= Tests for sklik_request =========

@patch("requests.post")
def test_sklik_request_success(mock_post):
    # Arrange: set up a fake successful response.
    fake_response = MagicMock(spec=requests.Response)
    fake_response.json.return_value = {"status": 200, "data": "success data"}
    mock_post.return_value = fake_response

    # Act:
    result = sklik_request("http://api.test", service="service", method="method", args=["arg1", "arg2"])

    # Assert:
    assert result == {"status": 200, "data": "success data"}
    expected_url = "http://api.test/service.method"
    mock_post.assert_called_once_with(url=expected_url, json=["arg1", "arg2"])


@patch("requests.post")
def test_sklik_request_error(mock_post):
    # Arrange: set up a fake error response.
    fake_response = MagicMock(spec=requests.Response)
    fake_response.url = "http://api.test/service.method"
    fake_response.json.return_value = {"status": 500, "statusMessage": "Server Error"}
    mock_post.return_value = fake_response

    # Act & Assert:
    with pytest.raises(SklikException):
        sklik_request("http://api.test", "service", "method", ["arg1"])


# ========= Tests for SklikApi class =========

@patch("sklik.api.sklik_request")
def test_sklikapi_init(mock_sklik_request):
    # Arrange: fake a successful login response.
    fake_response = {"status": 200, "session": "new_session_token"}
    mock_sklik_request.return_value = fake_response

    # Act: initialize the API.
    api = SklikApi.init("dummy_token")

    # Assert:
    assert api.session == "new_session_token"
    # Check that the default API is set.
    assert SklikApi.get_default_api() == api
    # Verify that sklik_request was called with the correct arguments.
    mock_sklik_request.assert_called_once_with(
        SKLIK_API_URL, service="client", method="loginByToken", args="dummy_token"
    )


def test_update_session():
    # Arrange:
    api = SklikApi("old_session")
    response = {"session": "updated_session"}

    # Act:
    api._update_session(response)

    # Assert:
    assert api.session == "updated_session"


def test_preprocess_call_none():
    api = SklikApi("test_session")
    result = api._preprocess_call(None)
    assert result == [{"session": "test_session"}]


def test_preprocess_call_with_userid():
    api = SklikApi("test_session")
    args = [{"userId": 123, "other": "value"}]
    result = api._preprocess_call(args)
    # The existing dict should be updated with the session.
    assert result[0]["session"] == "test_session"
    assert result[0]["userId"] == 123
    assert result[0]["other"] == "value"


def test_preprocess_call_without_userid():
    api = SklikApi("test_session")
    args = [{"some_key": "value"}]
    result = api._preprocess_call(args)
    # A session dict should be prepended.
    assert result[0] == {"session": "test_session"}
    assert result[1] == {"some_key": "value"}


@patch("sklik.api.sklik_request")
def test_call(mock_sklik_request):
    # Arrange:
    fake_response = {"status": 200, "session": "updated_session", "data": "result_data"}
    mock_sklik_request.return_value = fake_response
    api = SklikApi("old_session")
    args = [{"param": "value"}]

    # Act:
    result = api.call("test_service", "test_method", args)

    # Assert:
    # The _preprocess_call should have added the session dict.
    expected_payload = [{"session": "old_session"}] + args
    mock_sklik_request.assert_called_once_with(
        SKLIK_API_URL, "test_service", "test_method", expected_payload
    )
    # The session should have been updated.
    assert api.session == "updated_session"
    # And the result should match the fake response.
    assert result == fake_response
