<https://arxiv.org/pdf/2304.05028.pdf>

Modern read heavy data analytics rely on columnar data storage. Parquet and ORC spawned from Hadoop are dominant, but much has changed in the hardware and workloads in the last decade.
### Intro

Why is columnar storage used?
1. You can skip irrelevant attributes
2. You can compress data better
3. You can do parallel query processing

What has changed in the last decade?
1. SSD performance
2. Cloud storage usage: high bandwidth and latency
3. New better compression, indexing and filtering techniques

What does the paper do?
- Creates a realistic benchmark
- Does tests varying: encoding algos, block compression, metadata organization, index and filter and nested data modelling.

What were the general learnings?
- Parquet has faster column decoding, due to its encoding algo
- ORC does better selection pruning due to its zone maps
- Cheaper storage means we are moving to be more compute bound and we should use less aggressive compression
- We should avoid using block compression by default as the bandwidth savings don't outweigh the compute overhead
- Parquet/OCR only do basic data structure support with zone maps and bloom filters. We should do more here to precompute results.
- Parquet/OCR is not sufficient for ML workloads. Which do a lot of feature projections.
- Parquet/OCR don't utilise GPUs effectively. If we are using GPUs we want aggressive compression as I/O overhead dominates file scan time.

> What is selection pruning?
> - Just in SQL you select certain columns right? And in columnar storage as it's grouped in columns, its great at doing this as it only needs to read the column files which are selected.
> 
> What are dictionary codes?
> What are zone maps?
> What are bloom filters?

### Background
Hadoop introduced two row-oriented formats
- SequenceFile: Key value pairs
- Avro: JSON

>  What is vectorised processing?
>  What is late materialisation?

The history is that 
1. Meta released RCFile
2. Meta released ORC
3. Twitter Cloudera released Parquet

> What is record shredding?
> What is assembly algorithm from Dremel?
> What is google Capacitor format?
> What is Youtube Artus format? What makes it have constant seek time for nested schema?
> What is Meta DWRF format?
> What is Meta Alpha format?
> What is Arrow?

Lakehouse trend is to support better metadata management. For example ACID transactions. They add a metadata layer and do not directly modify the underlying columnar file formats.
- Delta Lake, Iceberg, Hudi

### Feature Taxonomy
#### Format Layout
Both Parquet and ORC use PAX format.

> What is PAX format?
> What is vectorised query processing?
> What is the tuple reconstruction overhead in a row group?
> What allows DuckDB and Arrow to perform parallel reads?

Both formats use lightweight encoding schemes to each column chunk. Then use general purpose block compression algorithms.

Entry point is the footer. Contains table schema and tuple count.


#### Encoding
Parquet and ORC support standard OLAP compression techniques
1. Dictionary encoding
2. run length encoding
3. Bitpacking

> What is dictionary encoding
> What is run length encoding
> What is bitpacking?

#### Compression
Both parquet and ORC enable block compression by default. And it seems that block compression is unhelpful for query speed.
#### Index and Filter
Parquet and ORC include zone maps and optional Bloom Filters to enable selection pruning. 

> What is a zone map?
> What are bloom filters?

Looks like spark enables pageIndex and bloom filters.
#### Nested Data Model
Open formats need to support nested data to support JSON and Protocol Buffers.

Parquet just takes nested data from Dremel.

> How does Dremel handle nested data?

###  Benchmarking
Standard OLAP benchmarks like SSB, TPC-H and TPC-DS generate datasets with uniform distributions. Some benchmarks do allow data skew, YCSB, DSB, BigDataBench, but often not sufficient. Real data is idea, but not comprehensive enough.

> What values does the benchmark care about?
> - Sortedness
> - Skew pattern
#### Column properties
What things matter about a column?
1. Number of distinct values: More compressible
2. Null ratio: Sparse data
3. Value range: bitpacking is affected by avg, variance of values
4. Sortedness: Affects encoding algo efficiency. (RLE, Delta)
5. Skew pattern: Frequency of values in a column. Are there hotspots?

#### Parameter distribution in real world data
Most data has a number of distinct values being 1% of total values.

Columnar data needs to handle both gentile and heavy hotspot skews.

Most integer values are small and therefore benefits from bitpacking.
### Experiments

#### Block compression
Block compression default does make S3 marginally faster but not by much. At the end of the day block compression dominates I/O of storage.

S3 specific optimisations we could do
- Store metadata continuously in the format to avoid multiple round trips
- Appropriately size the row groups or files to hide the access latency
- Coalescing small range requests to better utilise the cloud storage bandwidth

#### Scan with predicates

Zone maps are only useful on columns where values are well clustered.

Bloom filters are only useful for point queries.
- Bloom filters tell you if something does not exist in the data.
- Great for high selectivity queries.

We should consider more advanced techniques like 
- Column indexes
- Range filters

