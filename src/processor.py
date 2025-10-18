import logging
import apache_beam as beam
from src.conversation.conversation import Conversation
import enum

from src.messages.metrics import MessageMetricsResult

logger = logging.getLogger(__name__)


class ErrorMode(enum.Enum):
    RAISE = "raise"
    STOP = "stop"
    SKIP = "skip"


class ConversationProcessorFn(beam.DoFn):
    def __init__(self, error_mode: ErrorMode = ErrorMode.RAISE):
        self.error_mode = error_mode

    def process(self, conversation):
        logger.info(
            "Processing conversation by assignee_id: %s at created_at: %s",
            conversation.get("assignee_id"),
            conversation.get("created_at"),
        )
        try:
            conversation_obj = Conversation()
            for index, message in enumerate(conversation.get("messages", [])):
                content = message.get("body") or message.get("html_body") or ""

                if not content or not isinstance(content, str):
                    logging.warning(
                        f"Invalid message content in conversation by {conversation.get('assignee_id')} at {conversation.get('created_at')}"
                    )
                    content = ""

                message_metrics: MessageMetricsResult = conversation_obj.add_message(
                    content
                )
                for key, value in message_metrics.items():
                    conversation["messages"][index][key] = value

            conversation_metrics = conversation_obj.get_conversation_metrics()
            for key, value in conversation_metrics.items():
                conversation[key] = value
            yield conversation

        except Exception as e:
            logger.error(f"Error initializing Conversation object: {e}")
            if self.error_mode == ErrorMode.RAISE:
                raise
            elif self.error_mode == ErrorMode.STOP:
                return
            else:
                yield conversation
                return
