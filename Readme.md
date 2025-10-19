# Hashim's notes

## Technical documentation

### Prerequisites

- Docker
- Make (or execute commands manually)

### How to run locally
The application uses Docker and Makefile to simplify execution. I had a lot of problems in my machine (Windows) due to dependencies which required a lot of installation. I moved everything to Docker.

`make build` command will build the image for pipeline.

`make run-pipeline` command will execute the pipeline and generate output file.

`make test` For running the tests

`make lint` For checking the lint.

`make fmt` Format the files


### How to add new metric
### Message metrics

Message metrics are computed per message independently.

**File:** `src/messages/metrics.py`

**Steps:**
1. Create a class inheriting from `MessageMetric`
2. Implement `compute()` method
3. Implement `field_name` property
4. Add to `Message.__init__()` in `src/messages/message.py`

**Example:**

```python
class LengthMetric(MessageMetric):
    """Calculate message length"""
    
    @property
    def field_name(self) -> str:
        return "message_length"
    
    def compute(self, message: str) -> int:
        return len(message)
```

Then add to `Message` class:
```python
class Message:
    def __init__(self, content: str):
        self.metrics = [
            WordCountMetric(),
            ToneMetric(),
            LengthMetric(),  # ← Add here
        ]
```

### Conversation Metrics
Conversation metrics aggregate over messages to avoid double calculations.

**File:** `src/conversation/metrics.py`

**Steps:**
1. Create a class inheriting from `ConversationMetrics`
2. Implement `update()` to accumulate from each message
3. Implement `compute()` to finalize the value
4. Implement `field_name` property
5. Add to `Conversation.__init__()` in `src/conversation/conversation.py`

**Example:**

```python
class MessageCountMetric(ConversationMetrics):
    """Count total messages in conversation"""
    
    def __init__(self):
        self.count = 0
    
    @property
    def field_name(self) -> str:
        return "message_count"
    
    def update(self, message_metrics: MessageMetricsResult) -> None:
        self.count += 1
    
    def compute(self) -> int:
        return self.count
```

Then add to `Conversation` class:
```python
class Conversation:
    def __init__(self):
        self.metrics = [
            TotalWordCountMetric(),
            MinWordCountMetric(),
            MaxWordCountMetric(),
            AverageWordCountMetric(),
            ToneMetric(),
            MessageCountMetric(),  # ← Add here
        ]
```


### Future optimization for metrics
If the team needs quite often metrics management, I would go for CLI tool which creates basic templates registers the metric in corresponding class.

Another point for the metrics would be if they require external connections we might need to allow each metric to be able to dependend on another component such as `db_session` or `http_client` etc.

Plus if any metric might require previous calculation data from another metric, we have to make sure of linear ordering of metrics and using some dependency logic we can inject previous calculation data to avoid double calculations. It was overkill for this assignment so I didn't do it. 


### Research phase
First I had to understand the structure of the source data. That's why I added small cli command to give me basic stats.

Total 586 conversations and 11.737 total messages. I needed to know how is the distribution of messages per chat which could be useful argument while decision making. Average 20.03 message per conversation but we need to check the distribution.


Conversation Distribution (by message count):

   1-5 messages          161 ( 27.5%)

   6-10 messages          74 ( 12.6%)
   
   11-20 messages        151 ( 25.8%)
   
   21+ messages          200 ( 34.1%)


Why I am writing this is because of understanding does it make sense to parallelize conversations in long term planning. My understanding is that if we can avoid load imbalance yes. But current data size was not something to do very tiny improvements.


## Future improvements

### Short Term

1. **CLI Metric Generator**
   ```bash
   python -m src.cli.metric_generator --type message --name CustomMetric
   ```
   Auto-generates metric class template and registers it.

2. **Metric Dependencies**
   - Allow metrics to depend on previous metric calculations
   - Avoid duplicate calculations

3. **External Connections**
   - Inject `db_session`, `http_client` into metrics
   - Support metrics requiring external data


### Long Term

1. **Streaming for Large Data**
   - Switch from batch collection to streaming writes

2. **Balanced Bundling**
   - Bundle conversations by message count
   - Ensure even distribution across workers
   - Improves parallelization efficiency

3. **Runner Abstraction**
   - CLI option to select runner (Direct, Spark, Dataflow)

4. **Testing**
   - End-to-end integration tests
   - Performance benchmarks
   - Data quality validation tests

## Final words
Pipeline will generate 3 files.
- processed-data.json - Result of processing
- problematic-data.json - If any conversation fails to process will be written here
- process-stats.json - Will write overview

I loved the task even though I never did ML tasks (unless CS classes).

## Assignment
Please build a data pipeline that will:
* Read conversations data from `clean-data.json`
* Calculate the following metrics for each message:
	* `word_count`
	* `tone` - if the first word of the message has an odd number of letters, `tone` is negative, otherwise it's `positive`. Klaus' data scientists keep tweaking this algorithm to make it even more precise so this may change in the future.
* Calculate the following metrics for each conversation:
	* `total_word_count`
	* `min_message_word_count`
	* `max_message_word_count`
	* `average_message_word_count`
	* `tone` - the `tone` of the most messages in this conversation. If `positive` and `negative` messages are equal, set the conversation's `tone` to `mixed`
* Write the results into a file `processed-data.json` that has the same structure as the input file with the addition of the newly calculated fields.
* Anything that you can do to structure the pipeline in a way that makes it easier to add similar metrics in the future would be good.
* The starting point of an Apache Beam pipeline is provided but you can use any tool or framework you'd like.

Bonus:
* Create tests for the pipeline / the processing. Testing framework is up to you.