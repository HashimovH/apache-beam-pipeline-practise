import json
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from src.logging import setup_logging
from src.processor import ConversationProcessorFn, ErrorMode

logger = logging.getLogger(__name__)


def read_data():
    with open("clean-data.json", encoding="utf-8") as file:
        return json.loads(file.read())


class ConversationsToJsonFn(beam.DoFn):
    """Convert conversations to JSON format"""

    def process(self, element):
        yield json.dumps(element)


def run_pipeline():
    logger.info("Starting the Beam pipeline")
    options = PipelineOptions(["--runner=DirectRunner"])

    with beam.Pipeline(options=options) as p:
        (
            p
            | "ReadData" >> beam.Create(read_data())
            | "ProcessConversation" >> beam.ParDo(ConversationProcessorFn(error_mode=ErrorMode.SKIP))
            | "ConvertToJson" >> beam.ParDo(ConversationsToJsonFn())
            | "WriteOutput" >> beam.io.WriteToText(
                "output/processed-data.json",
                file_name_suffix="",
                shard_name_template="",
                append_trailing_newlines=True
            )
        )

    logger.info("Beam pipeline completed successfully")


if __name__ == "__main__":
    setup_logging()
    run_pipeline()
