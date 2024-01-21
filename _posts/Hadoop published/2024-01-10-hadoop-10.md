Hadoop Clusters
#### Cluster Setup
- Setup SSH
- Format HDFS: setup empty filesystem and creates namenode persistent data structures.

Starting and stopping Daemons
- Run scripts in `sbin`
- Keep note of the `slaves` file that contains all machine info, so you can do remote start and stopping

Creating user directories
- `hadoop fs -mkdir /user/username`

#### Hadoop Config
List of important files and config in `etc/hadoop` directory. Can have clones and specified using the `--config` flag.

Environment Vars
- `JAVA_HOME` (consider setting in hadoop-env.sh)
- namenode memory
- Consider moving hadoop logs to a different directory

#### Security
1. Kerberos only does authentication. Is the user actually who they claim to be.
2. Next need to do Authorisation: Is the user allowed?

Hadoop does access control with ACLs.
#### Benchmarking
Hadoop comes with several benchmarks you can run easily.
- TestDFSIO: I/O test
- MRBench: small jobs
- NNBench: load testing hardware
- Gridmix: tries to be realistic
- SWIM: actual real workloads
- TPCx-HS: standardized benchmark

```
hadoop jar \ $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \ teragen -Dmapreduce.job.maps=1000 10t random-data

then

hadoop jar \ $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \ terasort random-data sorted-data

then

hadoop jar \ $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \ teravalidate sorted-data report
```
