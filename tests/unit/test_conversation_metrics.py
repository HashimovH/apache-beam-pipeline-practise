from src.conversation.conversation import Conversation


def test_conversation_metrics_aggregation_basic():
    conv = Conversation()

    conv.add_message("Hello team")
    conv.add_message("I want to ask about my labels")
    conv.add_message("can we have manual labeling?")

    metrics = conv.get_conversation_metrics()

    assert metrics["total_word_count"] == 14
    assert metrics["min_message_word_count"] == 2
    assert metrics["max_message_word_count"] == 7
    assert metrics["average_message_word_count"] == 4.67
    assert metrics["tone"] == "negative"


def test_conversation_tone_mixed_on_tie():
    conv = Conversation()

    conv.add_message("even ok")
    conv.add_message("odd hi")

    metrics = conv.get_conversation_metrics()
    assert metrics["tone"] == "mixed"
