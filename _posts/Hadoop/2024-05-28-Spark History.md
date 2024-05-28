Why does it exist?
- Some Berkeley people realised Hadoop had limitations
- It doesn't separate compute and storage
- It doesn't support iterative algorithms
- So they created an RDD interface that lets you do much compute on
-<https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pd>

How can we make Spark support SQL?
- Initially you could do this with Shark, a hive fork.
- But this had issues
- It was over optimised for map reduce jobs.
- Also you could use Cloudera's Impala
- But now Databricks created SparkSQL shipped into the Spark runtime!
- Does some cool codegen that converts query clauses into ASTs which then generate JVM bytecode, which is invoked in scala.
- <https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf>

JVM had a lot of issues
- Lots of GC slowdowns
- Thats why the off heap exists, to avoid having to deal with GC.

So Databricks made it's own cpp execution engine.
- Uses Java Native Interface to invoke precompiled cpp code
-<https://people.eecs.berkeley.edu/~matei/papers/2022/sigmod_photon.pd>

How does spark optimise it's queries?
- Theres this thing called Catalyst that will convert your SQL query into
- a logical plan
- and then into 
- a physical plan

Spark also tries to modify the queries to help the queries
- It does adaptive query optimisations
- It changes the query plan before a stage starts based on observations from the preceding stage

How else can you accelerate spark?
- Apache Gluten
- RAPIDS accelerator for Spark
- Blaze
- Datafusion Comet
- All of these actually just get the physical plan from spark and ignore the Spark runtime and run it themselves

Creating all these parquet files sucks, how can this be easier?
- Delta Lake
- Kudu
- Hudi
- Iceberg
- Lets you write to these layers which calculates statistics and creates files for you