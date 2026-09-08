import pytest

from alert_engine import AlertEngine


def test_target_price_triggers_alert():
    decision = AlertEngine().evaluate(340, 350)
    assert decision.should_alert is True
    assert "target price reached" in decision.reasons


def test_significant_drop_triggers_alert():
    decision = AlertEngine(10).evaluate(90, 150, previous_price=100)
    assert decision.should_alert is True
    assert "price dropped 10.0%" in decision.reasons


def test_new_historical_low_triggers_alert():
    decision = AlertEngine().evaluate(80, 70, previous_lowest_price=90)
    assert decision.should_alert is True
    assert "new historical low" in decision.reasons


def test_no_rule_means_no_alert():
    decision = AlertEngine().evaluate(100, 90, previous_price=101, previous_lowest_price=95)
    assert decision.should_alert is False
    assert decision.reasons == ()


def test_invalid_threshold():
    with pytest.raises(ValueError):
        AlertEngine(0)
