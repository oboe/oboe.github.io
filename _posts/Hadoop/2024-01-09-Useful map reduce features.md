---
layout: post
tags: [Hadoop]
---
MapReduce Features

#### Counters
Best way to get metrics for your hadoop jobs. Theres a few variants
- Task Counters: aggregated metrics for all tasks
- Job Counters: job level metrics, like number of map tasks spawned
- Your own counters: metrics you can increment in your java code

#### Sorting
Using mapreduce to sort stuff is actually quite useful.
#### Joins
You can join large datasets but you should probs use a framework like Pig, Hive, Cascading, Cruc or Spark.
#### Side Data Distribution
Side data is extra readonly data you need during your tasks. Few ways to do this
- Job Config: you can set small KV pairs here. `JobConf`
- Distributed Cache: Can pass metadata with `-files` flag, which is copied at the start to your nodes and can be retrieved during your tasks.

#### Library Classes
Hadoop also provides prebuilt mappers and reducers to do basic stuff like select and map.