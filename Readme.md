# Hashim's notes

## Technical documentation

### How to run locally
The application uses Docker and Makefile to simplify execution. I had a lot of problems in my machine (Windows) due to dependencies which required a lot of installation. I moved everything to Docker.

`make build` command will build the image for pipeline.

`make run-pipeline` command will execute the pipeline and generate output file.

`make test` For running the tests

`make lint` For checking the lint.

`make fmt` Format the files


### How to add new metric
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


## Future architectural improvements

I have never worked with data pipelines so this thoughts are from my head.

- It is possible to make the runner CLI based so input and output files would have been provided.
- Depending on the size of input files, we can bundle the conversations based on message size so distribution would be balanced between workers
- One integration test could be added to test end to end reading, writing etc.
- In the writing part, I gather the results in the memory and write at once, this can be improved as well based on the input data size. 

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