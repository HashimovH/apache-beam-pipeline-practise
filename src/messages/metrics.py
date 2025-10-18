import abc
from typing import Any, TypedDict
import enum
import re
import logging

logger = logging.getLogger(__name__)

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
    WORD_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)
    def compute(self, message: str) -> int:
        return len(self.WORD_PATTERN.findall(message))

    @property
    def field_name(self) -> str:
        return "word_count"


class MessageToneMetric(MessageMetric):
    FIRST_WORD_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)
    
    def compute(self, message: str) -> MessageTone:
        first_word_match = self.FIRST_WORD_PATTERN.search(message)

        if not first_word_match:
            logger.error("Empty message received for tone computation.")
            return MessageTone.NEGATIVE
        
        first_word = first_word_match.group(0)
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
