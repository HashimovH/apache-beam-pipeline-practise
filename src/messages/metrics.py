import abc
from typing import Any, TypedDict
import enum
import re

# Precompiled regex to match ASCII letters only
_ASCII_LETTERS_RE = re.compile(r"[A-Za-z]")


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
        pass


class MessageWordCountMetric(MessageMetric):
    def compute(self, message: str) -> int:
        return len(message.split())

    @property
    def field_name(self) -> str:
        return "word_count"


class MessageToneMetric(MessageMetric):
    def compute(self, message: str) -> MessageTone:
        first_word = message.split()[0] if message.split() else ""
        # TBD: After answer from PM
        if len(first_word) % 2 == 0:
            return MessageTone.POSITIVE
        return MessageTone.NEGATIVE

    @property
    def field_name(self) -> str:
        return "tone"


# TODO: This could have been created with generated types for static type checking. but I skipped for the sake of simplicity.
class MessageMetricsResult(TypedDict):
    word_count: int
    tone: MessageTone
