

from src.messages.metrics import MessageTone, MessageToneMetric, MessageWordCountMetric


def test_message_word_count_basic():
    metric = MessageWordCountMetric()
    assert metric.field_name == "word_count"
    assert metric.compute(
        "Hello, I'm Hashim Zendesk client, I have a problem with task labels it shows {'error': 'internal server error'}") == 18


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


def test_message_tone_positive_when_first_word_length_even():
    metric = MessageToneMetric()
    assert metric.field_name == "tone"
    assert metric.compute("even hi") == MessageTone.POSITIVE


def test_message_tone_negative_when_first_word_length_odd():
    metric = MessageToneMetric()
    assert metric.compute("odd hi") == MessageTone.NEGATIVE


def test_message_tone_empty_message_defaults_positive():
    metric = MessageToneMetric()
    assert metric.compute("") == MessageTone.POSITIVE


def test_message_tone_single_character_word():
    metric = MessageToneMetric()
    assert metric.compute("A") == MessageTone.NEGATIVE
