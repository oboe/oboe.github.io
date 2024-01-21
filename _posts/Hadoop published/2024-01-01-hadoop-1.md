### Problems people have
The amount of data the world has is exploding. This is great as we can make better decisions with more data. But theres an issue. How can organisations store and process all this data?

**Problem 1**
The key bottleneck teams is facing is disk read. Reading disk (HDD) takes around 100MB/s and a SSD takes about 500MB/s. Reading a terabyte will take 2+ hours. This is way too slow. 😭

We can speed this up by parallelising disk reads.

**Problem 2**
But how do we do processing over the entire file if we are just reading portions? How do we combine this data?

MapReduce helps with this problem of combining and coordinating this data combining step.

**Hadoop tries to solve both these issues!**
### Other things Hadoop can do
So doing this batch processing is great but it still takes minutes to query data. So Hadoop/Apache has evolved to serve these needs as well.

**HBase** is a key value store that uses HDFS for its underlying storage.

**YARN** is a cluster resource management system that allows any distributed program to run on data in a Hadoop cluster. Thats amazing!

**Hive, Tez, Impala** can enable interactive SQL queries on Hadoop!

**Spark** enables iterative processing that needs a intermediate caching layer, instead of fetching from disk.

**Storm, Spark Streaming, Samza** enables running real time distributed compute on unbounded streams of data.

**Solr** can surprisingly run on a Hadoop cluster.

### What actually makes Hadoop different?
So Hadoop seems pretty useful. What makes it actually different to everything else?

Why can't we just use RDMS? In the past they were different but now they are getting much more similar. The differences being that RDBMS was optimised for small local read and writes. Meaning that it was normalised, indexed, followed a strict schema at write.

Why can't we just use those HPC clusters? Hadoop co-locates data with compute nodes so data access is fast. Hadoop also optimises network usage.