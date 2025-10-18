# Hashim Notes

## Research phase

First I had to understand the structure of the source data. That's why I added small cli command to give me basic stats.

Total 586 conversations and 11.737 total messages. I needed to know how is the distribution of messages per chat which could be useful argument while decision making. Average 20.03 message per conversation but we need to check the distribution.


Conversation Distribution (by message count):

   1-5 messages          161 ( 27.5%)

   6-10 messages          74 ( 12.6%)
   
   11-20 messages        151 ( 25.8%)
   
   21+ messages          200 ( 34.1%)


Why I am writing this is because of understanding does it make sense to parallelize conversations in long term planning. My understanding is that if we can avoid load imbalance yes. But current data size was not something to do very tiny improvements.



```
SPLIT TASKS:
  ├─ Pros: Parallelization, reusability, testability
  └─ Cons: Network shuffles, serialization overhead, complexity

KEEP TOGETHER:
  ├─ Pros: No shuffles, no serialization, simple
  └─ Cons: Can't parallelize, can't reuse, harder to test
```

## How to add new metric

### Message metrics

`src/messages/metrics.py` file contains the list of metrics for message resource. All metrics should follow the similar convention:

- Inherit from `MessageMetric` base class and implement the metods
- Suffix with `Metric` keyword for the class names.
- Add in the initialization method of `Message` class in `src/messages/message.py` file.

### Conversation Metrics
Conversation metrics are more advanced than message metrics because of aggregation and accumulation logic to avoid double calculations. 

`src/conversation/metrics.py` contains the logic of metrics.

```python

class ConversationMetrics(abc.ABC):
    """Base class for conversation-level metrics that accumulate over messages."""

    @abc.abstractmethod
    def update(self, message_metrics: MessageMetricsResult) -> None:
        """Update the metric with data from a new message."""
        pass

    @abc.abstractmethod
    def compute(self) -> Any:
        """Compute and return the final metric value."""
        pass

    @property
    @abc.abstractmethod
    def field_name(self) -> str:
        """Name of the metric field in output."""
        pass
```


- Inherit from `ConversationMetrics` base class and implement the metods
- Suffix with `Metric` keyword for the class names.
- Add in the initialization method of `Conversation` class in `src/conversation/conversation.py` file.

### Future optimization
If the team needs quite often metrics management, I would go for CLI tool which creates basic templates registers the metric in corresponding class.

Another point for the metrics would be if they require external connections we might need to allow each metric to be able to dependend on another component such as `db_session` or `http_client` etc.

Plus if any metric might require previous calculation data from another metric, we have to make sure of linear ordering of metrics and using some dependency logic we can inject previous calculation data to avoid double calculations. It was overkill for this assignment so I didn't do it. 


## How to setup locally
