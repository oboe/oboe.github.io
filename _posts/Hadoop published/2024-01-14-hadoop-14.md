Flume helps us ingest lots of data into Hadoop HDFS. 

Flume has sources, sinks which are connected with channels.
- Sources deliver events to channels
- Channels store events
- Sinks get events forwarded by channels
- similar ideas to kafka

#### Transactions and Reliability
At least once delivery.
#### The HDFS Sink
Can configure a HDFS sink that get all this flume data.

In use file has a `_` prefix. Good as HDFS ignores these files. Interesting as renaming is a costly operation in S3.
#### Fan Out
Often useful to have multiple channels for events. E.g having a secondary search sink.
#### Distribution: Agent Tiers
How is work distributed in Flume? It has tree structure. Some agents just collect data. Some agent aggregate this data.
#### Sink Groups
What do you do when an aggregating agent fails? Just load balance across them.