---
layout: post
tags: [Hadoop]
---
What are the main components of a map reduce job run?
1. The client
2. The YARN resource manager
3. The YARN node manager, which launches and monitors the compute containers on machines in the cluster
4. The MapReduce application master: keeps track of a mapreduce task and launches the required containers for the tasks
5. The distributed filesystem