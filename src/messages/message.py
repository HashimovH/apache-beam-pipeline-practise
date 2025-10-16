from typing import Any
from src.messages.metrics import MessageMetricsResult, MessageToneMetric, MessageWordCountMetric


class Message:
    def __init__(self, content: str):
        self.content = content
        self._metrics = [
            MessageWordCountMetric(),
            MessageToneMetric()
        ]
        self._computed_metrics: MessageMetricsResult = {}

    def compute_metrics(self) -> MessageMetricsResult:
        for metric in self._metrics:
            self._computed_metrics[metric.field_name] = metric.compute(
                self.content)
        return self._computed_metrics

    def get_metrics(self) -> MessageMetricsResult:
        return {
            field_name: self._computed_metrics.get(field_name)
            for field_name in self._computed_metrics
        }
