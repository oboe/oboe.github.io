---
layout: post
tags: [Hadoop]
---
Using MapReduce

### Configurations
Hadoop has a `Configuration` class for configurations.

If you want to switch between local running, distributed running it's recommended to keep these config files outside of the hadoop installation directory tree. You can do this by copying `etc/hadoop` dir somewhere else and setting `HADOOP_CONF_DIR` env var.

### Testing with MRUnit
MRUnit is a map reducing testing framework.

### Testing locally
Hadoop comes with a local job runner to run stuff locally in JVM, where you can use your debugger :D

### Running on a cluster
If you're running locally then you just need your classes on the same classpath, but if youre running distributed you need a single jar. How do we get a jar? We can use build tools like Ant and Maven to do this for us.

### Hadoop Logs

**Daemon logs**: a logfile and a stdout/stderr file.

**HDFS audit logs**: Log of all requests, turned off by default.

**MapReduce job history logs**: Log of events

**MapReduce task logs**: standard user jar errors and stuff.

### Hadoop Issues
- Try reproducing locally
- You can configure heap dumps
- You can profile tasks (HPROF profiler)

### Making shit faster
- How many mappers are you running and how long are they running for?
- How many reducers are you running and how long are they running for?
- Are you using combiners?
- Have you enabled map output compression?
- Are you doing custom serialization?
- Have you configured custom shuffling?

