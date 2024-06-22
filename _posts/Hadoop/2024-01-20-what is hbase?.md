---
layout: post
tags: [Hadoop]
---
HBase is a distributed column oriented database built on HDFS. Best for when you need random access to large data.

The canonical HBase use case is the webtable, a table of crawled web pages and their attributes, with billions of rows.  

HBase was modelled after Googles Bigtable.
#### Concepts
Data Models
- Tables have rows and columns.
- Columns are grouped into column families
- Column families are stored physically together
- Tables are partitioned into regions, a subset of rows.
- Row updates are atomic

HBase is built of clients, workers and a master.
- Master node orchestrates cluster of `regionserver` workers.
- `regionservers` carry zero or more regions
- HBase relies on zookeeper as authority on cluster state. Such as host vitals and current cluster master.

HBase tries to mirror Hadoop when it can. E.g with configs.
#### HBase vs RDBMS

What does it look scaling a RDBMS?
1. Move from local station to remotely hosted MySQL instance with well defined schema
2. Add memcached to cache common queries. Reads are not ACID anymore.
3. Scale MySQL vertically with a beefy server
4. Denormalise data to reduce joins
5. Stop doing server side compute
6. Periodically premateralize the most complete queries and stop joining in most cases
7. Drop secondary indexes and triggers
8. Maybe do more partitioning?

HBase 
1. No real indexes
2. Automatic partitioning
3. Scale linearly by adding new nodes
4. Commodity hardware
5. Fault tolerance
6. Batch processing

#### Praxis
HDFS was built for Hadoop MapReduce not HBase, so it runs into issues.
1. Running out of file descriptors. 1024
2. Running out of datanode threads.


