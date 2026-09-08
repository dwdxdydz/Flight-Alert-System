from unittest.mock import Mock, patch

import pytest

from data_manager import DataManager


def test_rejects_non_positive_timeout():
    with pytest.raises(ValueError, match="timeout must be positive"):
        DataManager("https://example.test", "token", timeout=0)


@patch("data_manager.requests.request")
def test_get_flight_data_rejects_a_non_list_prices_value(mock_request):
    response = Mock()
    response.json.return_value = {"prices": {"id": 1}}
    mock_request.return_value = response
    manager = DataManager("https://example.test", "token")

    with pytest.raises(ValueError, match="'prices' field must be a list"):
        manager.get_flight_data()

    response.raise_for_status.assert_called_once_with()
