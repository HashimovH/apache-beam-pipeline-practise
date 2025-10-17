#!/usr/bin/env python3
"""Simple CLI script to analyze clean-data.json and show summary statistics."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_conversations() -> list[dict]:
    """Load conversations from clean-data.json."""
    path = Path("clean-data.json")
    
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)
    
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        print(f"⚠️  File is empty: {path}")
        return []
    
    try:
        data = json.loads(text)
        if not isinstance(data, list):
            print(f"❌ Expected a list of conversations, got {type(data).__name__}")
            sys.exit(1)
        return data
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)


def print_summary(conversations: list[dict]) -> None:
    """Print summary statistics."""
    if not conversations:
        print("\n⚠️  No conversations found\n")
        return
    
    # Calculate message counts per conversation
    message_counts = [len(conv.get("messages", [])) for conv in conversations]
    total_messages = sum(message_counts)
    
    print("\n" + "="*60)
    print("📊 DATA SUMMARY")
    print("="*60)
    
    print(f"\n🗂️  Conversations: {len(conversations):,}")
    
    print(f"\n💬 Messages:")
    print(f"   Total:     {total_messages:,}")
    print(f"   Average:   {total_messages / len(conversations):.2f} per conversation")
    print(f"   Min:       {min(message_counts):,}")
    print(f"   Max:       {max(message_counts):,}")
    
    # Distribution histogram
    print(f"\n� Conversation Distribution (by message count):")
    
    buckets = {
        "0 messages": sum(1 for c in message_counts if c == 0),
        "1-5 messages": sum(1 for c in message_counts if 1 <= c <= 5),
        "6-10 messages": sum(1 for c in message_counts if 6 <= c <= 10),
        "11-20 messages": sum(1 for c in message_counts if 11 <= c <= 20),
        "21+ messages": sum(1 for c in message_counts if c > 20),
    }
    
    for bucket, count in buckets.items():
        if count > 0:
            pct = (count / len(conversations)) * 100
            bar = "█" * int(pct / 2)
            print(f"   {bucket:20s} {count:4d} ({pct:5.1f}%) {bar}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main entry point."""
    print("📁 Reading: clean-data.json")
    conversations = load_conversations()
    print_summary(conversations)


if __name__ == "__main__":
    main()
