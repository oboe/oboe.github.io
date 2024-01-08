YARN is Hadoops cluster resource management system, providing APIs for requesting cluster resources. MapReduce, Spark, Tez all call these APIs to run on the cluster. Pig, Hive, Crunch all run on these frameworks that build on YARN.

YARN is compromised of one resource manager and node managers which run on all nodes of the cluster.

Basic process is
1. you request to YARN resource manager
2. resource manager talks to node manager to start container
3. the container node manager starts container which includes the application process
4. container responds back to resource manager with heartbeat

Theres a few strategies to use YARN
1. Spark: You can start fixed number of YARN applications at the start and reuse these applications between workflows and user sessions. (For better caching and reuse)
2. MapReduce: You can start map tasks then later start reduce tasks. And do this each time for every new mapreduce workflow.
3. Slider, Impala: You can even just spawn one application for all users and reuse this for everything.


