import apache_beam as beam
import json


class ConversationsCollectorFn(beam.CombineFn):
    def create_accumulator(self):
        return []

    def add_input(self, accumulator, input):
        accumulator.append(input)
        return accumulator

    def merge_accumulators(self, accumulators):
        merged = []
        for acc in accumulators:
            merged.extend(acc)
        return merged

    def extract_output(self, accumulator):
        return json.dumps(accumulator, ensure_ascii=False, indent=2)
