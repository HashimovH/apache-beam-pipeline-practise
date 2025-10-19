import json
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from src.collector import ConversationsCollectorFn
from src.logging import setup_logging
from src.processor import ConversationProcessorFn
import time

logger = logging.getLogger(__name__)


def read_data():
    with open("clean-data.json", encoding="utf-8") as file:
        return json.loads(file.read())


def run_pipeline():
    start_time = time.time()
    logger.info("Starting the Beam pipeline")
    options = PipelineOptions(["--runner=DirectRunner"])

    with beam.Pipeline(options=options) as p:
        (
            p
            | "ReadData" >> beam.Create(read_data())
            | "ProcessConversation" >> beam.ParDo(ConversationProcessorFn())
            | "CollecConversation" >> beam.CombineGlobally(ConversationsCollectorFn())
            | "WriteOutput" >> beam.io.WriteToText(
                "processed-data.json",
                shard_name_template="",
                append_trailing_newlines=True
            )
        )

    logger.info("Beam pipeline completed successfully")
    duration = time.time() - start_time
    logger.info(f"Pipeline completed in {duration:.2f} seconds")


if __name__ == "__main__":
    setup_logging()
    run_pipeline()
