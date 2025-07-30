import pytest
from unittest.mock import MagicMock

from sklik.exception import SklikException
from sklik.api import SklikApi
from sklik.object import Account, AccountModel


# ========= Tests for AccountModel =========

def test_account_model_validation():
    # Data using API field names (camelCase) thanks to alias_generator.
    data = {
        "userId": 1,
        "username": "testuser",
        "walletCredit": 100,
        "walletCreditWithVat": 120,
        "walletVerified": True,
        "dayBudgetSum": 50,
        "accountLimit": 200
    }
    model = AccountModel.model_validate(data)
    assert model.user_id == 1
    assert model.username == "testuser"
    assert model.wallet_credit == 100

# ========= Fixtures for Report tests =========

@pytest.fixture
def fake_api():
    """A fake SklikApi with a mocked call method."""
    return MagicMock(spec=SklikApi)


# ========= Tests for Account._build_model and _find_account_data =========

def test_build_model_success(fake_api):
    # Create a dummy API response where the main "user" matches the account_id.
    dummy_response = {
        "user": {
            "userId": 1,
            "username": "testuser",
            "walletCredit": 100,
            "walletCreditWithVat": 120,
            "walletVerified": True,
            "dayBudgetSum": 50,
            "accountLimit": 200
        },
        "foreignAccounts": []
    }
    fake_api.call.return_value = dummy_response

    account = Account(account_id=1, api=fake_api)
    # _build_model is called in __init__; check that _model is built correctly.
    assert account._model.user_id == 1
    assert account._model.username == "testuser"


def test_build_model_failure(fake_api):
    # Create a dummy API response where neither "user" nor any foreign account matches.
    dummy_response = {
        "user": {
            "userId": 2,  # Does not match account_id 1.
            "username": "testuser",
            "walletCredit": 100,
            "walletCreditWithVat": 120,
            "walletVerified": True,
            "dayBudgetSum": 50,
            "accountLimit": 200
        },
        "foreignAccounts": []
    }
    fake_api.call.return_value = dummy_response

    with pytest.raises(SklikException) as exc_info:
        Account(account_id=1, api=fake_api)
    assert "Unable to fetch account data" in str(exc_info.value)


def test_find_account_data_user_match(fake_api):
    # Test that _find_account_data returns the 'user' part when the ID matches.
    dummy_response = {
        "user": {
            "userId": 1,
            "username": "testuser",
            "walletCredit": 100,
            "walletCreditWithVat": 120,
            "walletVerified": True,
            "dayBudgetSum": 50,
            "accountLimit": 200
        },
        "foreignAccounts": [
            {
                "userId": 2,
                "username": "foreign",
                "walletCredit": 200,
                "walletCreditWithVat": 240,
                "walletVerified": False,
                "dayBudgetSum": 70,
                "accountLimit": 300
            }
        ]
    }
    fake_api.call.return_value = dummy_response
    account = Account(account_id=1, api=fake_api)
    result = account._find_account_data(dummy_response)
    assert result == dummy_response["user"]


def test_find_account_data_foreign_match(fake_api):
    # Test that _find_account_data returns the matching foreign account if primary doesn't match.
    dummy_response = {
        "user": {
            "userId": 2,
            "username": "testuser",
            "walletCredit": 100,
            "walletCreditWithVat": 120,
            "walletVerified": True,
            "dayBudgetSum": 50,
            "accountLimit": 200
        },
        "foreignAccounts": [
            {
                "userId": 1,
                "username": "foreign",
                "walletCredit": 200,
                "walletCreditWithVat": 240,
                "walletVerified": False,
                "dayBudgetSum": 70,
                "accountLimit": 300
            }
        ]
    }
    fake_api.call.return_value = dummy_response
    account = Account(account_id=1, api=fake_api)
    result = account._find_account_data(dummy_response)
    assert result == dummy_response["foreignAccounts"][0]


# ========= Tests for __getattr__ =========

def test_getattr_delegation(fake_api):
    # Given that __getattr__ should forward attribute access to the underlying model:
    dummy_response = {
        "user": {
            "userId": 1,
            "username": "testuser",
            "walletCredit": 100,
            "walletCreditWithVat": 120,
            "walletVerified": True,
            "dayBudgetSum": 50,
            "accountLimit": 200
        },
        "foreignAccounts": []
    }
    fake_api.call.return_value = dummy_response
    account = Account(account_id=1, api=fake_api)

    # Account does not have a "username" attribute of its own, so it should come from _model.
    assert account.username == "testuser"

    # Test that an attribute not found in either Account or _model raises AttributeError.
    with pytest.raises(AttributeError) as exc_info:
        _ = account.non_existent_attribute
    assert "has no attribute 'non_existent_attribute'" in str(exc_info.value)


# ========= Account.call Tests =========

def test_call_method(fake_api):
    # Test that the Account.call method correctly prepends the userId and delegates to SklikApi.call.
    dummy_response = {
        "user": {
            "userId": 1,
            "username": "testuser",
            "walletCredit": 100,
            "walletCreditWithVat": 120,
            "walletVerified": True,
            "dayBudgetSum": 50,
            "accountLimit": 200
        },
        "foreignAccounts": []
    }
    fake_api.call.return_value = dummy_response

    account = Account(account_id=1, api=fake_api)

    # Reset the mock so that we can capture the call from the Account.call method.
    fake_api.call.reset_mock()

    # Define some arguments for the API call.
    args = [{"param": "value"}]
    # Simulate a successful API response.
    expected_api_response = {"result": "ok"}
    fake_api.call.return_value = expected_api_response

    result = account.call("service", "method", args)

    # The payload should prepend the user's ID from the model.
    expected_payload = [{'userId': account._model.user_id}] + args
    fake_api.call.assert_called_once_with("service", "method", expected_payload)
    assert result == expected_api_response
