import logging
import apache_beam as beam
from src.conversation.conversation import Conversation

from src.messages.metrics import MessageMetricsResult

logger = logging.getLogger(__name__)


class ConversationProcessorFn(beam.DoFn):
    def process(self, conversation):
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
            raise e
