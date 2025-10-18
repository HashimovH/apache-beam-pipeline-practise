import abc
from typing import Any, TypedDict
from src.messages.metrics import MessageMetricsResult, MessageTone
import enum


class ConversationTone(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"


class ConversationMetrics(abc.ABC):
    """Base class for conversation-level metrics that accumulate over messages."""

    @abc.abstractmethod
    def update(self, message_metrics: MessageMetricsResult) -> None:
        """Update the metric with data from a new message."""
        pass

    @abc.abstractmethod
    def compute(self) -> Any:
        """Compute and return the final metric value."""
        pass

    @property
    @abc.abstractmethod
    def field_name(self) -> str:
        """Name of the metric field in output."""
        pass

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the metric state for a new conversation."""
        pass


class TotalWordCountMetric(ConversationMetrics):
    """Accumulates total word count across all messages in a conversation."""

    def __init__(self):
        self._total = 0

    def update(self, message_metrics: MessageMetricsResult) -> None:
        word_count = message_metrics.get("word_count", 0)
        self._total += word_count

    def compute(self) -> int:
        return self._total

    @property
    def field_name(self) -> str:
        return "total_word_count"

    def reset(self) -> None:
        self._total = 0


class MinMessageWordCountMetric(ConversationMetrics):
    """Tracks minimum word count among all messages in a conversation."""

    def __init__(self):
        self._min = None

    def update(self, message_metrics: MessageMetricsResult) -> None:
        word_count = message_metrics.get("word_count", 0)
        if self._min is None or word_count < self._min:
            self._min = word_count

    def compute(self) -> int:
        return self._min if self._min is not None else 0

    @property
    def field_name(self) -> str:
        return "min_message_word_count"

    def reset(self) -> None:
        self._min = None


class MaxMessageWordCountMetric(ConversationMetrics):
    """Tracks maximum word count among all messages in a conversation."""

    def __init__(self):
        self._max = 0

    def update(self, message_metrics: MessageMetricsResult) -> None:
        word_count = message_metrics.get("word_count", 0)
        if word_count > self._max:
            self._max = word_count

    def compute(self) -> int:
        return self._max

    @property
    def field_name(self) -> str:
        return "max_message_word_count"

    def reset(self) -> None:
        self._max = 0


class AverageMessageWordCountMetric(ConversationMetrics):
    """Calculates average word count across all messages in a conversation."""

    def __init__(self):
        self._total = 0
        self._count = 0

    def update(self, message_metrics: MessageMetricsResult) -> None:
        word_count = message_metrics.get("word_count", 0)
        self._total += word_count
        self._count += 1

    def compute(self) -> float:
        return round(self._total / self._count if self._count > 0 else 0.0, 2)

    @property
    def field_name(self) -> str:
        return "average_message_word_count"

    def reset(self) -> None:
        self._total = 0
        self._count = 0


class ConversationToneMetric(ConversationMetrics):
    """Determines conversation tone based on majority of message tones."""

    def __init__(self):
        self._positive_count = 0
        self._negative_count = 0

    def update(self, message_metrics: MessageMetricsResult) -> None:
        tone = message_metrics.get("tone")
        if tone == MessageTone.POSITIVE:
            self._positive_count += 1
        elif tone == MessageTone.NEGATIVE:
            self._negative_count += 1

    def compute(self) -> ConversationTone:
        if self._positive_count > self._negative_count:
            return ConversationTone.POSITIVE
        elif self._negative_count > self._positive_count:
            return ConversationTone.NEGATIVE
        else:
            return ConversationTone.MIXED

    @property
    def field_name(self) -> str:
        return "tone"

    def reset(self) -> None:
        self._positive_count = 0
        self._negative_count = 0


# TODO: Similaryly this can be generated small script instead.
class ConversationMetricsResult(TypedDict):
    total_word_count: int
    min_message_word_count: int
    max_message_word_count: int
    average_message_word_count: float
    tone: str
