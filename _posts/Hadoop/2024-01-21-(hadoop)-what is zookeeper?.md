ZooKeeper is Hadoops distributed coordination service. It can't make partial failures go away but it can help you handle partial failures.
- Its simple, a stripped down filesystem that exposes a few simple operations
- Its expressive, it can be used to build coordination data structures and protocols
- Its available, applications can depend on it
- It helps loosely coupled interactions, helps computers find other finders
- its a library, It lets open source use tried and tested protocols

#### Example
How can we have an actively maintained list of active servers?
- With zookeeper you can
- You have znodes, that form a hierarchical namespace. e.g `/zoo` and `/zoo/duck`

#### ZooKeeper service

Data Model
- Data access is atomic. In reads and writes. No partial failures.
- Znodes can be ephemeral or persistent. Ephemeral nodes are deleted when creating client session ends.
- You can have sequential znodes, where file paths are generated with numbers. This gives you clear global ordering!
- You can create watches. One off znode change notification alerts!

Zookeeper service runs on a cluster. Gets high availability with replication.
- If 2/5 nodes fail its fine.
- Uses Zab protocol to do this (leader election, atomic broadcast)

All updates to znode tree have a globally unique identifier.

#### Building applications with ZooKeeper
Zookeeper comes with prebuilt distributed data structures and protocols you can use.
- barriers
- queues
- two phase commits
