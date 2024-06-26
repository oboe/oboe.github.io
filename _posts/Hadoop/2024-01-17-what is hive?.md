---
layout: post
tags: [Hadoop]
---
Hive is a framework for data warehousing on top of Hadoop. Hive enables SQL jockeys to process massive data.
#### Installing Hive
Similar to pig. Hive runs locally and converts your SQL queries into Hadoop jobs. To help with this HDFS schema and metadata is stored in its own metastore.

You can interact with Hive with the Hive Shell. 
- pretty magical to just write a SQL query and process massive data

#### Running Hive
Similar config as Hadoop.

Originally Hive written to use MapReduce as execution engine but now can use Tez and Spark (DAG engines).
- DAG engines can often avoid intermediate HDFS writes!

#### Comparison with Traditional Databases
Hive is kinda morphing into a traditional database, but theres a bunch of decisions underpinned by its original HDFS and MapReduce origins.

Schema on Read vs Schema on Write
- Traditional DBs enforce table scheme on write, Hive doesnt.
- Means that hive has much faster initial load, no need to parse, read and crap.
- Also means that general queries are slower, no column indexing or compression.

Updates, Transactions, Indexes
- These are general traditional DB concepts. 
- You can do it now in hive.
- Can't really do in place file updates well so handles it with delta files.
- Also supports table locking with ZooKeeper.

SQL on Hadoop others
- Cloudera Impala: performance improvement to Hive, by running daemons on datanodes.
- Hive has improved performance by supporting Tez!
- Others: Presto, Drill, Spark

#### HiveQL
Pretty much SQL with Hadoop specific commands like Transform, Map, Reduce.

#### Tables
Hive tables have the data and the metadata.
- Data is stored in HDFS or S3
- Metadata stored in relational DB