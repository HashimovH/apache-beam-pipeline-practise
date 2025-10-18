from src.messages.metrics import MessageWordCountMetric


def test_message_word_count_basic():
    metric = MessageWordCountMetric()
    assert metric.field_name == "word_count"
    assert (
        metric.compute(
            "Hello, I'm Hashim Zendesk client, I have a problem with task labels it shows {'error': 'internal server error'}"
        )
        == 19
    )


def test_message_word_count_multiple_spaces_behavior():
    metric = MessageWordCountMetric()
    assert metric.compute("Hello   world") == 2


def test_message_word_count_empty_string():
    metric = MessageWordCountMetric()
    assert metric.compute("") == 0


def test_message_word_count_only_spaces():
    metric = MessageWordCountMetric()
    assert metric.compute("     ") == 0


def test_message_word_count_single_word():
    metric = MessageWordCountMetric()
    assert metric.compute("Hello") == 1


def test_message_word_count_special_characters():
    metric = MessageWordCountMetric()
    assert metric.compute("Hello, world! This is a test.") == 6

    assert metric.compute("Hello... Are you there???") == 4

    assert metric.compute("Well-done is better than well-said.") == 7

    assert metric.compute("C'est la vie!") == 4
