

from src.messages.metrics import MessageTone, MessageToneMetric


def test_message_tone_positive_when_first_word_length_even():
    metric = MessageToneMetric()
    assert metric.field_name == "tone"
    assert metric.compute("even hi") == MessageTone.POSITIVE


def test_message_tone_negative_when_first_word_length_odd():
    metric = MessageToneMetric()
    assert metric.compute("odd hi") == MessageTone.NEGATIVE


def test_message_tone_empty_message_defaults_positive():
    metric = MessageToneMetric()
    assert metric.compute("") == MessageTone.NEGATIVE



def test_message_tone_single_character_word():
    metric = MessageToneMetric()
    assert metric.compute("A") == MessageTone.NEGATIVE
