import abc
from typing import Any, TypedDict
import enum


class MessageTone(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class MessageMetric(abc.ABC):
    @abc.abstractmethod
    def compute(self, message: str) -> Any:
        pass

    @property
    @abc.abstractmethod
    def field_name(self) -> str:
        """Name of the metric field in output"""
        pass


class MessageWordCount(MessageMetric):
    def compute(self, message: str) -> int:
        return len(message.split(' '))

    @property
    def field_name(self) -> str:
        return "word_count"


class MessageToneAnalysis(MessageMetric):
    def compute(self, message: str) -> MessageTone:
        first_word = message.split()[0].lower() if message else ""
        if len(first_word) % 2 == 1:
            return MessageTone.NEGATIVE
        return MessageTone.POSITIVE

    @property
    def field_name(self) -> str:
        return "tone"


# TODO: This could have been created with generated types for static type checking. but I skipped for the sake of simplicity.
class MessageMetricsResult(TypedDict):
    word_count: int
    tone: MessageTone
