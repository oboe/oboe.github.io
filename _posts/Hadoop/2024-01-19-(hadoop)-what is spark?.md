Spark is a cluster computing framework for data processing. 
- It doesnt use MapReduce
- Great at keeping large datasets in memory between jobs. (Unlike mapreduce which loads data every time)
- Making it great at iterative algorithms and interactive analysis
- Also has a great DAG engine that can process arbitrary pipelines into single jobs.

#### Example
Resilient Distributed Datasets are read only object collections that you play with in Spark.

Jobs run in applications. Each interactive spark session is an application. Jobs can access cached data from previous jobs.

#### Resilient Distributed Datasets
You can create these by
1. From memory objects
2. External datasets
3. Transforming existing RDDs

You can aggregate RDD by keys with `ReduceByKey()`, `foldByKey()` and `aggregateByKey()`.

You can cache RDDs by calling `cache()`!
- Can also choose depth of persistence with `persist()`

Usually data is just serialised with Java serialisation.
- Just implement `Serializable`, simple
- Can also use Kryo serialization 

#### Shared Variables
How do we access data outside of RDDs?

We can use broadcast variables. Variables that are stored in cache across jobs.

We can also use Accumulators. Kinda like counters. After jobs are completed, these accumulator info can be retrieved.

#### Anatomy of a Spark Job Run
Fairly simple driver contains application info which runs executors.

Tasks are either `Shuffle map tasks` or `Result tasks`.
#### Executors and Cluster Managers
Cluster managers manage the executors.
- Local: JVM
- Standalone: runs a single spark master with workers
- Mesos: general purpose manager
- YARN: you know it