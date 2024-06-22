---
layout: post
tags: [Hadoop]
---
So with a lot of data Hadoop needs a way to store it reliably across a fleet of machines. Thats what the HDFS does.

HDFS is a distributed filesystem, optimised for read heavy workloads.

## Blocks
Blocks are the min unit for reading and writing data. Disk blocks are usually 512 and file blcoks are usually few KB. Hadoop blocks are usually 128MB. Big HDFS blocks to reduce time spent doing disk seeks to start of block.

```
How to list blocks:
hdfs fsck / -files -blocks
```

## Namenodes and Datanodes
HDFS has two types of nodes operating in master worker pattern. Namenodes are masters, datanodes are workers.

Namenode
- Managers filesystem namespace
- Maintains filesystem tree and metadata for all files and directories
- Maintains what datanodes have what blocks
- Persisted to disk as namespace image and edit log

Datanode
- Store, retrieve blocks
- Report to namenode with lists of blocks they store

When the namenode is lost, we're fucked
- So we can write namenode info to multiple filesystems
- And have a secondary namenode which just periodically merges namespace image with edit log. Fancy way to say that it does checkpointing.

We can run multiple namenodes that each manage a namespace volume
- Just partitioning

We can also run multiple nodes for higher availability
- One is on standby
- The two nodes need highly available shared storage for edit log, usually using Quorum Journal Manager that runs a few journal nodes, where each log is committed to the majority of nodes. Similar to ZooKeeper.
- Having multiple nodes is a pain when a node goes down. Failover controller just manages this, still has to go to great lengths in ungracegful handover to stop misbehaving node at all costs.

## The CLI
Pretty much the same as unix.
- Just add -ls or -mkdir after hadoop fs

## Hadoop filesystems
HDFS is one implementation of the hadoop filesystem. `org.apache.hadoop.fs.FileSystem` 

```
How to talk to other implementations.
hadoop fs -ls s3a:///
```

How important is data locality really?

Hadoop can only write to the end of the file. Hadoop cannot do random modifications of a file.

**What is FUSE**
Filesystem in Userspace allows filesystems that are implemented in user space to be integrated as Unix filesystems.

## The Java Interface
You can read data with URLs specifying an URL `FsUrlStreamHandlerFactory`

Get a `FileSystem` then you can open, seek, read, create, append files and directories.

From that get a `FileStatus` that you can get all the file and directory metadata. 

## Data Flow
**Read**
Pretty simple, opening a file with HDFS, talks to namenode first to get block locations of datanodes, then talks to the relevant datanodes.

**Write**
Talks to namenode, starts writing to the `FSDataOutputStream` that writes packets to a pipeline of datanodes. Each datanodes passes data to next replication datanode. When all datanodes acknowledge they've written a packet then the packet is complete.

**Huh**
Content written to a file is not guaranteed to be visible even if stream is flushed. A block of data needs to be written or you need to call `hflush` or `hsync` for it to be persisted.

## Parallel Copying with `distcp`
`hadoop distcp file1 file2`
This is pretty cool it just does a mapreduce without reduce to copy stuff.