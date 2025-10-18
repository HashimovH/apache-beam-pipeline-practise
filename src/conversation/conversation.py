from src.messages.message import Message
from src.conversation.metrics import (
    ConversationMetrics,
    ConversationMetricsResult,
    TotalWordCountMetric,
    MinMessageWordCountMetric,
    MaxMessageWordCountMetric,
    AverageMessageWordCountMetric,
    ConversationToneMetric
)
from src.messages.metrics import MessageMetricsResult


class Conversation:
    def __init__(self):
        self._metrics: list[ConversationMetrics] = [
            TotalWordCountMetric(),
            MinMessageWordCountMetric(),
            MaxMessageWordCountMetric(),
            AverageMessageWordCountMetric(),
            ConversationToneMetric()
        ]
        self._metric_values = {
            metric.field_name: None for metric in self._metrics}

    def add_message(self, message_content: str) -> MessageMetricsResult:
        message = Message(message_content)
        message_metrics = message.compute_metrics()

        for metric in self._metrics:
            metric.update(message_metrics)

        return message_metrics

    def get_conversation_metrics(self) -> ConversationMetricsResult:
        return {
            metric.field_name: metric.compute()
            for metric in self._metrics
        }

    def to_dict(self) -> ConversationMetricsResult:
        return {
            **self.get_conversation_metrics()
        }
