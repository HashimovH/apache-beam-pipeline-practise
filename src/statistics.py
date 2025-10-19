import apache_beam as beam
import json

from collections import Counter


class StatsCollectorFn(beam.CombineFn):
    def create_accumulator(self):
        return {
            "num_conversations": 0,
            "total_messages": 0,
            "tone_distribution": Counter(),
        }

    def add_input(self, acc, conversation):
        acc["num_conversations"] += 1
        acc["total_messages"] += len(conversation.get("messages", []))
        acc["tone_distribution"][conversation.get("tone", "unknown")] += 1
        return acc

    def merge_accumulators(self, accs):
        merged = self.create_accumulator()
        for a in accs:
            merged["num_conversations"] += a["num_conversations"]
            merged["total_messages"] += a["total_messages"]
            merged["tone_distribution"].update(a["tone_distribution"])
        return merged

    def extract_output(self, acc):
        acc["tone_distribution"] = dict(acc["tone_distribution"])
        return json.dumps(acc, ensure_ascii=False, indent=2)
