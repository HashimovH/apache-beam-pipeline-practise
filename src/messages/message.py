from typing import Any, cast

from src.messages.metrics import (
    MessageMetricsResult,
    MessageToneMetric,
    MessageWordCountMetric,
)


class Message:
    def __init__(self, content: str):
        self.content = content
        self._metrics = [MessageWordCountMetric(), MessageToneMetric()]
        self._computed_metrics: dict[str, Any] = {}

    def compute_metrics(self) -> MessageMetricsResult:
        for metric in self._metrics:
            self._computed_metrics[metric.field_name] = metric.compute(self.content)
        return cast(MessageMetricsResult, self._computed_metrics)

    def get_metrics(self) -> MessageMetricsResult:
        return cast(MessageMetricsResult, self._computed_metrics)
