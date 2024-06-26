---
layout: post
tags: [Hadoop]
---
Hadoop Admin
#### HDFS
`% hdfs dfsadmin` is a tool that helps find info about the state of HDFS. 

`% hdfs fsck` tool to check health of files.
- easy to use to check what blocks are in any particular file

#### Monitoring
The thing you should most care about is the master daemons: namenodes and resource manager.

All hadoop daemons log. You can set log levels in webUI `/logLevel` and with CLI or in `log4j.properties` file.
```
hadoop daemonlog -setlevel resource-manager-host:8088 \ org.apache.hadoop.yarn.server.resourcemanager DEBUG
```

View stack traces in web UI `/stacks`

View metrics with JConsole as they are published to JMX. Or through web UI `/jmx`
#### Maintenance
Taking snapshots, a copy of filesystem subtree is enough to reconstruct filesystem contents.
