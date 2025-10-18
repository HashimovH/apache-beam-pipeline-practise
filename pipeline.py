import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from src.processor import ConversationProcessorFn, ErrorMode


def read_data():
    with open("clean-data.json", encoding="utf-8") as file:
        return json.loads(file.read())


def get_conversations():
    """Return a list of conversation dicts regardless of top-level shape."""
    data = read_data()
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("conversations"), list):
        return data["conversations"]
    return []


class ConversationsToJsonFn(beam.DoFn):
    """Convert conversations to JSON format"""

    def process(self, element):
        yield json.dumps(element)


conversations = get_conversations()

if not conversations:
    with open("processed-data.json", "w", encoding="utf-8") as f:
        f.write("[]\n")
else:
    options = PipelineOptions(["--runner=DirectRunner"])

    with beam.Pipeline(options=options) as p:
        (
            p
            | "ReadData" >> beam.Create(conversations)
            | "ProcessConversation" >> beam.ParDo(ConversationProcessorFn(error_mode=ErrorMode.SKIP))
            | "ConvertToJson" >> beam.ParDo(ConversationsToJsonFn())
            | "WriteOutput" >> beam.io.WriteToText(
                "output/processed-data.json",
                file_name_suffix="",
                shard_name_template="",
                append_trailing_newlines=True
            )
        )
