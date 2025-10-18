from apache_beam.testing.util import assert_that, equal_to
from apache_beam.testing.test_pipeline import TestPipeline
import apache_beam as beam
from src.conversation.metrics import ConversationTone
from src.messages.metrics import MessageTone
from src.processor import ConversationProcessorFn, ErrorMode


def test_dofn_processor():
    input_data = [
        {
            "id": "conv_1",
            "messages": [{"html_body": "Hi there"}, {"html_body": "Hello world!"}],
        },
        {
            "id": "conv_2",
            "messages": [
                {"html_body": "This is a test."},
                {"html_body": "Beam is great for data processing."},
            ],
        },
    ]

    expected_output = [
        {
            "id": "conv_1",
            "messages": [
                {
                    "html_body": "Hi there",
                    "word_count": 2,
                    "tone": MessageTone.POSITIVE,
                },
                {
                    "html_body": "Hello world!",
                    "word_count": 2,
                    "tone": MessageTone.NEGATIVE,
                },
            ],
            "total_word_count": 4,
            "min_message_word_count": 2,
            "max_message_word_count": 2,
            "average_message_word_count": 2.0,
            "tone": ConversationTone.MIXED,
        },
        {
            "id": "conv_2",
            "messages": [
                {
                    "html_body": "This is a test.",
                    "word_count": 4,
                    "tone": MessageTone.POSITIVE,
                },
                {
                    "html_body": "Beam is great for data processing.",
                    "word_count": 6,
                    "tone": MessageTone.POSITIVE,
                },
            ],
            "total_word_count": 10,
            "min_message_word_count": 4,
            "max_message_word_count": 6,
            "average_message_word_count": 5.0,
            "tone": ConversationTone.POSITIVE,
        },
    ]

    with TestPipeline() as p:
        input_pcoll = p | beam.Create(input_data)

        output_pcoll = input_pcoll | beam.ParDo(
            ConversationProcessorFn(error_mode=ErrorMode.SKIP)
        )

        assert_that(output_pcoll, equal_to(expected_output))
