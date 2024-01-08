Hadoop I/O

### Corruption
With large data, corruption is guaranteed to happen, hadoop uses CRC-32 checksums to detect this. Datanodes and clients verify all the data they receive with checksums. We also have a `DataBlockScanner` which unsurprisingly scans data blocks for bit corruption. When clients notice corruption, it snitches to the namenode and the namenode schedules a new block replica.

### Compression
Just a tradeoff decision between compression speed and size. Also should consider if the compression format is splittable. Splittable means that you can seek to any point and start reading. Important for MapReduce! 

You'll need to download these compression codec libaries. 
- e.g `org.apache.hadoop.io,compress.DefaultCodec`

### Serialisation 
Data into byte streams. Hadoop uses `Writable` its own serialisation format. Usually MapReduce programs will use `Writable` key and value types.

### File based data structures
Writing each file is a pain, so Hadoop has some convenience containers. `SequenceFile`, `MapFile`, `SetFile`, `ArrayFile`, `BloomMapFile`
```
easy way to see compressed, sequence files, avro etc in hadoop
hadoop fs -text file | head
```

**Row oriented files**
Just each row pretty much appended together. A1,A2,B1,B2. SequenceFile, MapFile, Avro are all row oriented.

**Column oriented files**
Chunks of each column appended together. A1,B1,A2,B2. RCFile, ORCFile, Parquet are all column oriented.