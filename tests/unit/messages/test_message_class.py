from src.messages.message import Message
from src.messages.metrics import MessageTone


def test_message_compute_metrics_contains_expected_fields_and_values():
    msg = Message(
        "hello dear support team, I am stuck in the password change loop")
    metrics = msg.compute_metrics()

    assert "word_count" in metrics
    assert "tone" in metrics

    assert isinstance(metrics["word_count"], int)
    assert metrics["word_count"] == 12
    assert metrics["tone"] == MessageTone.NEGATIVE


def test_message_get_metrics_matches_compute_metrics():
    msg = Message("Hello dear support, I'm having issues logging in.")
    computed = msg.compute_metrics()
    retrieved = msg.get_metrics()
    assert computed == retrieved
